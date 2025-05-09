from model import Transformer
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from DataLoader import SensorDataset
import logging
import time
from plot import *
from helpers import *
from joblib import load
from icecream import ic
from torch.optim.lr_scheduler import ReduceLROnPlateau
import math, random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)
logger = logging.getLogger(__name__)


def flip_from_probability(p):
    return True if random.random() < p else False


def transformer(
    dataloader,
    EPOCH,
    k,
    frequency,
    path_to_save_model,
    path_to_save_loss,
    path_to_save_predictions,
    device="cpu",
):
    device = torch.device(device)
    model = Transformer().double().to(device)
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.MSELoss()
    best_model = ""
    min_train_loss = float("inf")

    for epoch in range(EPOCH + 1):
        train_loss = 0
        model.train()

        for index_in, index_tar, _input, target, sensor_number in dataloader:
            optimizer.zero_grad()
            src = _input.permute(1, 0, 2).double().to(device)[:-1, :, :]
            target = _input.permute(1, 0, 2).double().to(device)[1:, :, :]
            sampled_src = src[:1, :, :]

            for i in range(len(target) - 1):
                prediction = model(sampled_src)

                if i < 24:
                    prob_true_val = True
                else:
                    v = k / (k + math.exp(epoch / k))
                    prob_true_val = flip_from_probability(v)

                if prob_true_val:
                    sampled_src = torch.cat(
                        (sampled_src.detach(), src[i + 1, :, :].unsqueeze(0).detach())
                    )
                else:
                    positional_encodings_new_val = src[i + 1, :, 1:].unsqueeze(0)
                    predicted_humidity = torch.cat(
                        (
                            prediction[-1, :, :].unsqueeze(0),
                            positional_encodings_new_val,
                        ),
                        dim=2,
                    )
                    sampled_src = torch.cat(
                        (sampled_src.detach(), predicted_humidity.detach())
                    )

            loss = criterion(target[:-1, :, 0].unsqueeze(-1), prediction)
            loss.backward()
            optimizer.step()
            train_loss += loss.detach().item()

        if train_loss < min_train_loss:
            torch.save(
                model.state_dict(), path_to_save_model + f"best_train_{epoch}.pth"
            )
            torch.save(
                optimizer.state_dict(), path_to_save_model + f"optimizer_{epoch}.pth"
            )
            min_train_loss = train_loss
            best_model = f"best_train_{epoch}.pth"

        if epoch % 10 == 0:
            logger.info(f"Epoch: {epoch}, Training loss: {train_loss}")
            scaler = load("scalar_item.joblib")
            sampled_src_humidity = scaler.inverse_transform(sampled_src[:, :, 0].cpu())
            src_humidity = scaler.inverse_transform(src[:, :, 0].cpu())
            target_humidity = scaler.inverse_transform(target[:, :, 0].cpu())
            prediction_humidity = scaler.inverse_transform(
                prediction[:, :, 0].detach().cpu().numpy()
            )
            plot_training_3(
                epoch,
                path_to_save_predictions,
                src_humidity,
                sampled_src_humidity,
                prediction_humidity,
                sensor_number,
                index_in,
                index_tar,
            )

        train_loss /= len(dataloader)
        log_loss(train_loss, path_to_save_loss, train=True)

    plot_loss(path_to_save_loss, train=True)
    return best_model
