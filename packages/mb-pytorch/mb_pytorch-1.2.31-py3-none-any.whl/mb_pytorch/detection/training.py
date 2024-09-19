import torch
from typing import Optional
import tqdm
import os
from mb_utils.src.logging import logger
import numpy as np
from ..utils.viewer import gradcam_viewer,plot_classes_pred,plot_to_image
from mb_pytorch.models.modelloader import ModelLoader
from mb_pytorch.training.train_params import train_helper
from mb.plt.utils import dynamic_plt

__all__ = ['detection_train_loop']

def detection_train_loop( k_yaml: dict,scheduler: Optional[object] =None,writer: Optional[object] =None,
                              logger: Optional[object] =None,gradcam: Optional[object] =None,
                              gradcam_rgb: str =False,device: str ='cpu'):
    """
    Function to train the model
    Args:
        k_yaml: data dictionary YAML of DataLoader
        scheduler: scheduler
        writer: tensorboard writer
        logger: logger
        gradcam: gradcam layers to be visulized
        device: default is cpu
    output:
        None
    """
    
    if logger:
        logger.info('Training loop Starting')
    k_data = k_yaml.data_dict['data']
    data_model = k_yaml.data_dict['model']
    model_data_load = ModelLoader(k_yaml.data_dict['model'])
    model =  model_data_load.get_model()
    device_type = data_model['device']
    bbox_threshold = data_model['model_meta_data']['model_bbox_threshold']

    if logger:
        logger.info('Model Loaded')
    
    train_loader,val_loader,_,_ = k_yaml.data_load()
    loss_attr,optimizer_attr,optimizer_dict,scheduler_attr,scheduler_dict = train_helper(data_model) 
    optimizer = optimizer_attr(model.parameters(),**optimizer_dict)
    if scheduler is not None:
        scheduler = scheduler_attr(optimizer,**scheduler_dict)

    if logger:
        logger.info('Optimizer and Scheduler Loaded')
        logger.info(f'Loss: {loss_attr}')
        logger.info(f'Optimizer: {optimizer}')
        logger.info(f'Scheduler: {scheduler}')

    if device_type =='cuda':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if device == 'cuda':
            torch.cuda.empty_cache()
            if logger:
                logger.info('Device: CUDA')
                logger.info(torch.cuda.get_device_name(0))

    model.to(device)
    best_val_loss = float('inf')

    for epoch in tqdm.tqdm(range(data_model['model_epochs']), desc="Epochs"):
        
        ##train loop
        
        model.train(True)
        train_loss = 0
        
        if logger:
            logger.info('Training Started')
        for batch_idx, data in enumerate(tqdm.tqdm(train_loader, desc="Training", leave=False)):
            images,bbox,labels = data.values()
            images = list(image.to(device) for image in images)
            bbox = list(b.to(device) for b in bbox)
            bbox = [b.view(-1, 4) if b.dim() == 1 else b for b in bbox]
            labels = list(label.to(device) for label in labels)  
            targets = [{'boxes': b,'labels': label} for b,label in zip(bbox, labels)]      
                    
            optimizer.zero_grad()
            loss_dict = model(images, targets)  
            losses = sum(loss for loss in loss_dict.values())
            
            losses.backward()
            optimizer.step()
            if scheduler is not None:
                scheduler.step()
            
            train_loss += losses.item()
            if logger:
                logger.info(f'Epoch {epoch+1} - Batch {batch_idx+1} - Train Loss: {losses.item()}')
        
        avg_train_loss = train_loss / len(train_loader)
        if logger:
            logger.info(f'Epoch {epoch+1} - Train Loss: {avg_train_loss}')
            logger.info(f"lr = {optimizer.param_groups[0]['lr']}")

        model.train(False)

        ## Validation loop
        val_loss = 0
        val_bbox = []
        val_labels = []
        val_scores = []
        val_targets_labels = []
        val_targets_bbox = []

        with torch.no_grad():
            for batch_idx, data in enumerate(tqdm.tqdm(val_loader, desc="Validation", leave=False)):
                images,bbox,labels = data.values()
                images = list(image.to(device) for image in images)
                bbox = list(b.to(device) for b in bbox)
                bbox = [b.view(-1, 4) if b.dim() == 1 else b for b in bbox]
                labels = list(label.to(device) for label in labels)  
                targets = [{'boxes': b,'labels': label} for b,label in zip(bbox, labels)]    

                loss_dict = model(images, targets)  ## output is boxes, labels, scores

                if len(loss_dict) == 0:
                    continue
                else:
                    for i in range(len(loss_dict)):
                        if len(loss_dict[i]['boxes']) > 0 :
                            if 'scores' in loss_dict[i]:
                                for j in range(len(loss_dict[i]['scores'])):
                                    if loss_dict[i]['scores'][j] > bbox_threshold:
                                        val_bbox.append(loss_dict[i]['boxes'][j])
                                        val_labels.append(loss_dict[i]['labels'][j])
                                        val_scores.append(loss_dict[i]['scores'][j])
                                        if j < 1:
                                            val_targets_labels.append(labels[i])
                                            val_targets_bbox.append(bbox[i])

                #losses = sum(loss for loss in loss_dict.values() if loss.numel()>0)
                
                val_loss += losses.item() * len(images)
                if logger: 
                    logger.info(f'Epoch {epoch+1} - Batch {batch_idx+1} - Val Loss: {losses.item()}')
            
            avg_val_loss = val_loss / len(val_loader.dataset)
            
            if logger:
                logger.info(f'Epoch {epoch+1} - Avg Val Loss: {avg_val_loss:.3f}')

        # TensorBoard logging
        if writer is not None:
            writer.add_scalar('Loss/train', avg_train_loss, global_step=epoch)
            writer.add_scalar('Loss/val', avg_val_loss, global_step=epoch)
            writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], global_step=epoch)
            
            for name, param in model.named_parameters():
                writer.add_histogram(name, param, global_step=epoch)
            
            # Visualizations
            if len(images) > 0:
                img_l = [np.array(i.to('cpu')) for i in images]
                labels_l = [str(list(np.array((l.to('cpu'))))[0]) for l in labels] ##check for multiple labels
                #create_img_grid(x, x, writer, global_step=epoch)
                fig = dynamic_plt(img_l,labels=labels_l,bboxes=val_targets_bbox,return_fig=True)
                writer.add_image('grid', plot_to_image(fig), global_step=epoch)

                # # Grad-CAM visualization 
                # if gradcam is not None:
                #     use_cuda = 'cpu'
                #     for cam_layers in gradcam:
                #         grad_img = gradcam_viewer(cam_layers, model, img_l.unsqueeze(0), gradcam_rgb=gradcam_rgb, use_cuda=use_cuda) 
                #         if grad_img is not None:
                #             grad_img = np.transpose(grad_img, (2, 0, 1))
                #             writer.add_image(f'Gradcam/{cam_layers}', grad_img, global_step=epoch)
                #         elif logger:
                #             logger.info(f'Gradcam not supported for {cam_layers}')   
   
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            best_model = model.state_dict()

            path = os.path.join(os.path.dirname(k_data['file']['root']), 'best_model.pth')
            torch.save(best_model, path)
            if logger:
                logger.info(f'Epoch {epoch + 1} - Best Model Saved (Val Loss: {best_val_loss:.4f})')