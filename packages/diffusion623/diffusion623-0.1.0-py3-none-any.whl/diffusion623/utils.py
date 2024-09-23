
import wandb
import torch

from .trainer import Trainer
from .unet import Unet

# fix random seed for reproducibility
torch.manual_seed(2024)
torch.cuda.manual_seed(2024)
torch.cuda.manual_seed_all(2024)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

def setup_diffusion(args, Diffusion=None):
    if Diffusion is None:
        from diffusion import Diffusion
    
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )

    model = Unet(
        dim=args["unet_dim"],
        dim_mults=args["unet_dim_mults"],
    ).to(device)

    diffusion = Diffusion(
        model,
        image_size=args["image_size"],
        channels=3,
        timesteps=args["time_steps"],  # number of steps
    ).to(device)

    trainer = Trainer(
        diffusion,
        args["data_path"],
        image_size=args["image_size"],
        train_batch_size=args["batch_size"],
        train_lr=args["learning_rate"],
        train_num_steps=args["train_steps"],  # total training steps
        gradient_accumulate_every=2,  # gradient accumulation steps
        results_folder=args["save_folder"],
        load_path=args["load_path"],
        dataset="train",
        data_class=args["data_class"],
        device=device,
        save_and_sample_every=args["save_and_sample_every"],
        fid=args["fid"],
        dataloader_workers=args['dataloader_workers']
    )

    return model, diffusion, trainer



def train_diffusion(args, Diffusion=None):
    wandb.login()
    wandb.init(
        project="DDPM_AFHQ",
        config=args,
        reinit=True,
        name=args["save_folder"].split("/")[-1],
    )

    _, _, trainer = setup_diffusion(args, Diffusion=Diffusion)

    trainer.train()


def visualize_diffusion(args, Diffusion=None):
    wandb.login()
    wandb.init(
        project="DDPM_AFHQ",
        config=args,
        reinit=True,
        name=args["save_folder"].split("/")[-1],
    )

    _, _, trainer = setup_diffusion(args, Diffusion=Diffusion)
    
    trainer.visualize_diffusion()
