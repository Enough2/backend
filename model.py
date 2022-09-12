import torch
import torchvision.transforms as transforms
import torchvision.models as models


class Pipeline:
    def __init__(self):
        self.classes = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
        self.transformations = transforms.Compose(
            [transforms.Resize((256, 256)), transforms.ToTensor()]
        )

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.model = self.to_device(Model(self.classes), self.device)
        self.model.load_state_dict(
            torch.load("resnet152_0813.pt", map_location=self.device)
        )
        self.model.eval()

    def to_device(self, data, device):
        return data.to(device, torch.float32)

    def predict_image(self, image):
        tensor = self.transformations(image)
        xb = self.to_device(tensor.unsqueeze(0), self.device)
        yb = self.model(xb)
        return {self.classes[i]: float(yb[0][i]) for i in range(len(self.classes))}


class Model(torch.nn.Module):
    def __init__(self, classes):
        super().__init__()
        self.network = models.resnet152(weights="DEFAULT")
        self.network.fc = torch.nn.Linear(self.network.fc.in_features, len(classes))

    def forward(self, xb):
        return torch.sigmoid(self.network(xb))
