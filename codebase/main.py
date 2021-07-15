
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
    def doing():
        #train # vielleicht noch um uncertainty erweitern
            #train_acc_hist, train_loss_hist , train_evidence_hist = train_model(model, dataloaders["train"], criterion, optimizer, model_directory, device , num_classes =10,  num_epochs=num_epochs ,uncertainty= False)
            val_acc_hist1 = eval_model(model, dataloaders["TESTCIFAR90"],model_directory ,device, num_classes=90)
            val_acc_hist1 = eval_model(model, dataloaders["TESTCIFAR100"],model_directory ,device, num_classes=100)
            val_acc_hist = eval_model(model, dataloaders["val"],model_directory ,device, num_classes=10)
            #also plot for that

            # saves the histogramms 
            #save_Plot(train_loss_hist,train_evidence_hist,val_acc_hist,val_acc_hist1, model_directory)

    parser = argparse.ArgumentParser() # easy commandline | options 
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--train", action="store_true",
                            help="To train the network.")
    #einfacher beides gleichzeitig zu machen
    mode_group.add_argument("--eval", action="store_true",
                            help="To evaluate the network.")
    parser.add_argument("--epochs", default=25, type=int,
                        help="Desired number of epochs.")
    parser.add_argument("--pretrained", default=False, action="store_true",
                        help="Use a pretrained model.")
    #parser.add_argument("--dropout", action="store_true",
    #                    help="Whether to use dropout or not.")
    parser.add_argument("--uncertainty",default=False , action="store_true",
                        help="Use uncertainty or not.")
    parser.add_argument("--crossEntropy", default=False ,action="store_true",
                        help="Sets loss function to Cross entropy Loss.")                        
    ## noch vorer untersuchen wie uncertainty funktioniert was ist mit u ? 
    # wird irgendwie anders trainiert als normal um uncertainty zu berechen
    # probieren mit uncertainty = True bei tain_model()
    #uncertainty_type_group = parser.add_mutually_exclusive_group()
    #uncertainty_type_group.add_argument("--mse", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Expected Mean Square Error.")
    #uncertainty_type_group.add_argument("--digamma", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Expected Cross Entropy.")
    #uncertainty_type_group.add_argument("--log", action="store_true",
    #                                    help="Set this argument when using uncertainty. Sets loss function to Negative Log of the Expected Likelihood.")

    args = parser.parse_args()

    if args.train:
        num_epochs = args.epochs
        
        model = models.resnet18(pretrained=args.pretrained)
        # adapt it to our Data
        model.fc = nn.Linear(512, 10)

        device = get_device()
        if args.crossEntropy:
            # wo das modell gespeichet wird
            model_directory = "CrossEntropyLoss/"
            criterion = nn.CrossEntropyLoss()
        #elif args.otherCriteron:
            #criterion = otherCriterion()
        else: 
            print("pls choose a criterion")
            raise RuntimeError('please choose Criterion')
        #for folder naming
        #if args.dropout:
        #    model_directory = model_directory[:-1] +"Dropout/" 
        
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
            
            doing()
        # pretrained = false
        else: #(theoretisch auch optimizer parsen) aber brauche ich noch nicht
            optimizer = Adam(model.parameters())
            
            doing()
    #elif args.eval:

            #val_acc_hist = eval_model(model, dataloaders["TESTCIFAR90"], model_directory, device, num_classes=10)


if __name__ == "__main__":
    main()
    # TODO:
    # Uncertainty how does it work ? 
    # test on Notebook
    
