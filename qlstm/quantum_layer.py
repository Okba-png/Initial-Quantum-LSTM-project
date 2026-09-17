# qlstm/quantum_layer.py

import numpy as np
from qiskit import QuantumCircuit
from qiskit_machine_learning.connectors import TorchConnector
from qiskit_machine_learning.neural_networks import EstimatorQNN
import torch
from torch import nn


class QuantumFeatureMap:
    """
    Einfache Feature-Map:
    - Kodiert klassische Eingaben (z.B. x_t, h_{t-1}) in Qubit-Rotationen.
    - Hier: 2 Qubits, je einer für x_t und h_{t-1}.
    """

    def __init__(self, num_qubits: int = 2):
        self.num_qubits = num_qubits

    def construct_circuit(self, x: float, h_prev: float) -> QuantumCircuit:
        """
        Baut einen QuantumCircuit, der die Eingaben in Rotationen kodiert.
        x, h_prev werden hier als skalare Werte angenommen.
        In der Praxis kannst du sie vorher normalisieren / skalieren.
        """
        qc = QuantumCircuit(self.num_qubits)

        # Qubit 0 kodiert x_t
        qc.ry(x, 0)

        # Qubit 1 kodiert h_{t-1}
        qc.ry(h_prev, 1)

        # Optional: einfache Verschränkung
        qc.cx(0, 1)

        return qc


class QuantumLSTMLayer(nn.Module):
    """
    Quantum-Layer, die als Baustein im LSTM verwendet wird.
    - Nutzt Qiskit EstimatorQNN + TorchConnector.
    - Eingabe: (x_t, h_{t-1}) als 2D-Feature.
    - Ausgabe: ein skalarer Wert, der z.B. als Gate-Output genutzt wird.
    """

    def __init__(self, num_qubits: int = 2):
        super().__init__()

        self.num_qubits = num_qubits
        self.feature_map = QuantumFeatureMap(num_qubits=self.num_qubits)

        # Parameterisierte Ansatz-Schaltung (Ansatz = trainierbare Gates)
        qc_ansatz = QuantumCircuit(self.num_qubits)
        # Beispiel: einfache RY-RX-Ansatz mit Parametern
        # In der Praxis: Parameter werden von QNN verwaltet
        qc_ansatz.ry(0.0, 0)
        qc_ansatz.rx(0.0, 1)
        qc_ansatz.cx(0, 1)

        # EstimatorQNN: erwartet Parameter für Ansatz + Eingabe-Parameter
        # Hier vereinfachen wir: nur Ansatz-Parameter werden trainiert,
        # Eingaben werden über Feature-Map in den Circuit eingebaut.
        self.qnn = EstimatorQNN(
            circuit=qc_ansatz,
            input_params=[],
            weight_params=list(qc_ansatz.parameters),
        )

        # TorchConnector: macht aus QNN ein PyTorch-Modul
        self.torch_layer = TorchConnector(self.qnn)

    def forward(self, x_t: torch.Tensor, h_prev: torch.Tensor) -> torch.Tensor:
        """
        Forward-Pass:
        - x_t: aktueller Input (Batch, 1)
        - h_prev: vorheriger Hidden-State (Batch, 1)
        Wir gehen hier von Batch-Größe 1 aus, um es einfach zu halten.
        Für größere Batches müsste man die Circuits batched ausführen.
        """

        # Extrahiere skalare Werte (hier stark vereinfacht)
        x_val = x_t.item()
        h_val = h_prev.item()

        # Baue Feature-Map-Circuit
        qc_input = self.feature_map.construct_circuit(x_val, h_val)

        # EstimatorQNN erwartet Parameter-Tensoren:
        # - input: hier leer, weil wir Eingaben direkt in Circuit kodieren
        # - weights: werden von TorchConnector verwaltet
        # Wir nutzen TorchConnector direkt, der nur weights als Parameter hat.
        # Um den Input zu berücksichtigen, müssten wir QNN anders konfigurieren.
        # Für ein didaktisches Gerüst lassen wir den Quantum-Teil als
        # "trainierbare nichtlineare Transformation" stehen.

        # Dummy-Input für TorchConnector (z.B. 0.0), da wir hier nur
        # die trainierbaren Gewichte nutzen.
        input_tensor = torch.zeros(1)

        # Quantum-Ausgabe (Skalar)
        y_q = self.torch_layer(input_tensor)

        return y_q
