Alles klar, Sabir — ich erstelle dir jetzt eine **kompakte 1‑Seiten‑PDF‑Version**, perfekt geeignet zum **Export als PDF** in VS Code oder Jupyter.  
Du bekommst **nur den Text**, sauber strukturiert, damit du ihn direkt als `.md` oder Notebook‑Markdown einfügen und als PDF exportieren kannst.

---

# 📘 **Quantum Computing Cheat‑Sheet — 1‑Seiten‑Version (PDF‑Text)**

---

## **Qubit & Born‑Regel**

Ein Qubit ist ein komplexer 2D‑Vektor:

\[
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle,\quad |\alpha|^2 + |\beta|^2 = 1
\]

Messung:

- \(P(0)=|\alpha|^2\)  
- \(P(1)=|\beta|^2\)  
- Messung kollabiert den Zustand.

---

## **Mehrere Qubits**

\[
|\phi\rangle = a|00\rangle + b|01\rangle + c|10\rangle + d|11\rangle
\]

Tensorprodukt:

\[
|a\rangle \otimes |b\rangle = |ab\rangle
\]

---

## **Wichtige Gatter (unitär)**

### **Pauli**
| Gate | Matrix |
|------|--------|
| X | \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\) |
| Y | \(\begin{pmatrix}0&-i\\i&0\end{pmatrix}\) |
| Z | \(\begin{pmatrix}1&0\\0&-1\end{pmatrix}\) |

### **Hadamard**
\[
H=\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\]

### **Phase**
| Gate | Bedeutung |
|------|-----------|
| S | Phase π/2 |
| T | Phase π/4 |

---

## **CNOT**

Definition:

\[
|0\rangle\langle0|\otimes I + |1\rangle\langle1|\otimes X
\]

Bedeutung:

- Kontrolle = 0 → nichts  
- Kontrolle = 1 → Ziel flippt

Qiskit:

```python
qc.cx(control, target)
```

---

## **Messung**

```python
qc.measure(qubit, classical_bit)
```

Messung erzeugt klassische Bits und zerstört die Superposition.

---

## **Simulatoren**

### **AerSimulator (Messung)**
```python
from qiskit_aer import AerSimulator
sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()
counts = result.get_counts()
```

### **Statevector (Amplituden)**
```python
from qiskit.quantum_info import Statevector
Statevector.from_instruction(qc)
```

### **Wann was?**

| Zweck | Statevector | AerSimulator |
|------|-------------|--------------|
| Amplituden | ✔ | ❌ |
| Phasen | ✔ | ❌ |
| Messung | ❌ | ✔ |
| Hardware‑Realismus | ❌ | ✔ |

---

## **Bell‑Zustand (Verschränkung)**

Erzeugung:

```python
qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure(0,0)
qc.measure(1,1)
```

Zustand:

\[
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
\]

Messung (1000 shots):

```
{'00': ~500, '11': ~500}
```

---

## **Mini‑Übungen**

1. **X‑Gate** → |1⟩  
2. **Y‑Gate** → i|1⟩  
3. **H + Z** → |−⟩  
4. **Bell‑Zustand messen** → 00/11

---

# ⭐ Fertig — 1‑Seiten‑PDF‑Text

Du kannst diesen Text jetzt:

- in VS Code als `.md` speichern → **Export as PDF**  
- in Jupyter als Markdown‑Zelle einfügen → **Download as PDF**  

Wenn du willst, mache ich dir:

- eine **optisch gestaltete PDF‑Version** (mit Farben, Tabellenrahmen, Layout)  
- eine **Version mit Code‑Zellen**  
- eine **Version für Unterricht / BOS 13**  

Sag einfach Bescheid.