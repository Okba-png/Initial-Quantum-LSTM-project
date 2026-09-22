import torch
from torch import nn, optim
from qlstm.hybrid_qlstm import HybridQuantumLSTM


def generate_dummy_sequence_data(num_samples=100, seq_len=10):
    """
    Erzeugt einfache Dummy-Daten:
    - Eingabe: Sequenzen von Zufallszahlen.
    - Ziel: Summe der Sequenz (Regression).
    """
    X = torch.randn(num_samples, seq_len, 1)
    y = X.sum(dim=1)  # (num_samples, 1)
    return X, y


def train_model():
    # Hyperparameter
    num_samples = 200
    seq_len = 10
    num_epochs = 20
    lr = 1e-3

    # Daten
    X, y = generate_dummy_sequence_data(num_samples=num_samples, seq_len=seq_len)

    # Modell
    model = HybridQuantumLSTM(input_size=1, hidden_size=16, num_layers=1)

    # Verlustfunktion und Optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training
    for epoch in range(num_epochs):
        model.train()

        optimizer.zero_grad()
        y_pred = model(X)  # (num_samples, 1)
        loss = criterion(y_pred, y)

        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {loss.item():.4f}")


if __name__ == "__main__":
    train_model()
