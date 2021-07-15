import torch.nn as nn
from torch.nn.functional import dropout
from torch.optim import Adam
import torchvision.models as models
import argparse


from helpers import get_device
from train import train_model
from data import dataloaders
from eval import eval_model, save_Plot



def main():
    """
    Example for running : python main.py --crossEntropy
    must have: 
    can have: 
              --pretrained (trained on a model with pretrained weights) # Default pretrained = False
              --uncertrainty (when using an uncertaintyLoss)            # Default uncertainty =False
                    (Example: --mse //NOT INPLEMENTET YET) 
              --epochs (how may epochs for training)                    # Default epochs = 25
              --$LOSS (specifiy Loss Example : --crossEntropy)          # Default --crossEntropy
    """
    #########EXPERIMENTS#################
    def CIFAR10_eval_on_CIFAR100(ignoreThreshold, train=False):
        """
        train= true: Trains Resnet with parameters specified with argument (--pretrained, --$loss ...)
        Evaluates on CIFAR10
        Evaluates on CIFAR90
        Evaluates on CIFAR100
        """
        if train:
            train_acc_hist, train_loss_hist , train_uncertainty_hist = train_model(model, dataloaders["train"], criterion, optimizer, model_directory, device , num_classes =10,  num_epochs=num_epochs ,uncertainty= False, ignoreThreshold =ignoreThreshold)
        
        val_acc_hist, uncertainty_history = eval_model(model, dataloaders["TESTCIFAR90"],model_directory ,device, num_classes=90)
        val_acc_hist, uncertainty_history = eval_model(model, dataloaders["TESTCIFAR100"],model_directory ,device, num_classes=100)
        val_acc_hist, uncertainty_history = eval_model(model, dataloaders["val"],model_directory ,device, num_classes=10)

        # saves the histogramms 
        #save_Plot(train_loss_hist,train_uncertainty_hist, val_acc_hist, val_acc_hist1, model_directory)

        print("\n Experint: CIFAR10_eval_on_CIFAR100 DONE \n")

    def runExperiments():
        """
        Runs Experiments specified
        """
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.4 , train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.45 ,train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.5 , train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.6 , train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.7 , train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.8 , train = False )
        CIFAR10_eval_on_CIFAR100(ignoreThreshold =0.9 , train = False )

        print("DONE with all expretiments")

           
    parser = argparse.ArgumentParser() # easy commandline | options 
    parser.add_argument("--epochs", default=25, type=int,
                        help="Desired number of epochs.")
    parser.add_argument("--pretrained", default=False, action="store_true",
                        help="Use a pretrained model.")
    parser.add_argument("--uncertainty",default=False , action="store_true",
                        help="Use uncertainty or not.")
    parser.add_argument("--crossEntropy", default=False ,action="store_true",
                        help="Sets loss function to Cross entropy Loss.")                        

    #uncertainty_type_group = parser.add_mutually_exclusive_group()
    #uncertainty_type_group.add_argument("--mse", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Expected Mean Square Error.")
    #uncertainty_type_group.add_argument("--digamma", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Expected Cross Entropy.")
    #uncertainty_type_group.add_argument("--log", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Negative Log of the Expected Likelihood.")

    args = parser.parse_args()

    
    num_epochs = args.epochs
        
    model = models.resnet18(pretrained=args.pretrained)
    # adapt it to our Data
    model.fc = nn.Linear(512, 10)

    device = get_device()
    if args.crossEntropy:

        # Where the model will be saved
        model_directory = "CrossEntropyLoss/"
        criterion = nn.CrossEntropyLoss()

    #elif args.otherCriteron:
        #criterion = otherCriterion()
    
    #DEFAULT
    else: 
       # Where the model will be saved
        model_directory = "CrossEntropyLoss/"
        criterion = nn.CrossEntropyLoss()
    
    if args.pretrained:
    
        model_directory = model_directory[:-1] +"Pretrained/"  
        all_parameters = list(model.parameters())
        #we want last layer to have a faster learningrate 
        without_lastlayer =all_parameters[0: len(all_parameters) -2] # -2 weil einmal weiht und einmal Bias vom layer
        #so we extract it
        last_param = model.fc.parameters()

        #passing a nested dict for different learningrate with differen params
        optimizer = Adam([
            {'params': without_lastlayer},
            {'params': last_param, 'lr': 1e-3}
            ], lr=1e-2)
            
        runExperiments()
    # pretrained = False
    else: 
        optimizer = Adam(model.parameters())
        
        runExperiments()


if __name__ == "__main__":
    main()
    
    
    
