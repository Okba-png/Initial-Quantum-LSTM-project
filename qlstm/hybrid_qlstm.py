# qlstm/hybrid_qlstm.py

import torch
from torch import nn
from .quantum_layer import QuantumLSTMLayer


class HybridQuantumLSTM(nn.Module):
    """
    Hybrides Quantum-LSTM-Modell:
    - Klassisches LSTM für Sequenzverarbeitung.
    - Quantum-Layer als zusätzlicher nichtlinearer Baustein,
      der Gate-ähnliche Informationen liefert.
    """

    def __init__(self, input_size: int = 1, hidden_size: int = 16, num_layers: int = 1):
        super().__init__()

        self.hidden_size = hidden_size

        # Klassisches LSTM
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )

        # Quantum-Layer (arbeitet auf skalarer Projektion des Hidden-States)
        self.quantum_layer = QuantumLSTMLayer(num_qubits=2)

        # Lineare Ausgabe-Schicht
        self.fc = nn.Linear(hidden_size + 1, 1)  # +1 für Quantum-Output

    def forward(self, x: torch.Tensor):
        """
        x: Eingabe-Sequenz (Batch, SeqLen, InputSize)
        Beispiel: Batch=1, SeqLen=T, InputSize=1
        """

        batch_size, seq_len, _ = x.size()

        # Initial Hidden- und Cell-State
        h0 = torch.zeros(1, batch_size, self.hidden_size)
        c0 = torch.zeros(1, batch_size, self.hidden_size)

        # Klassisches LSTM
        lstm_out, (hn, cn) = self.lstm(x, (h0, c0))
        # lstm_out: (Batch, SeqLen, HiddenSize)

        # Wir nehmen den letzten Zeitschritt
        h_last = lstm_out[:, -1, :]  # (Batch, HiddenSize)

        # Reduziere Hidden-State auf einen Skalar pro Batch (z.B. Mittelwert)
        h_scalar = h_last.mean(dim=1, keepdim=True)  # (Batch, 1)

        # Quantum-Layer: nutzt letzten Input und Hidden-Scalar
        # Hier: letzter Input x[:, -1, 0]
        x_last = x[:, -1, 0]  # (Batch,)
        # Für Einfachheit: nur Batch=1
        q_out = self.quantum_layer(x_last[0].unsqueeze(0), h_scalar[0].unsqueeze(0))
        # q_out: Skalar (Tensor mit Shape (1,))

        # Kombiniere klassischen Hidden-State mit Quantum-Output
        # Erweitere q_out auf Batch-Dimension
        q_out_expanded = q_out.view(1, 1)  # (Batch=1, 1)
        combined = torch.cat([h_last, q_out_expanded], dim=1)  # (Batch, HiddenSize+1)

        # Finale Ausgabe
        y = self.fc(combined)  # (Batch, 1)

        return y
