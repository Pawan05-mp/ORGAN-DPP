# ORGAN-DPP: 5-Minute Video Script

**Total Runtime: 5 minutes (300 seconds)**
**Pacing: ~2 minutes per 500 words**

---

## **SECTION 1: INTRODUCTION (0:00-0:30)**
*30 seconds*

**[Visual: Show drug molecules on screen, animated transformations]**

**Narration:**
"What if you could generate thousands of drug-like molecules in seconds? ORGAN-DPP is an AI system that does exactly that. It generates novel molecular structures automatically—and evaluates each one across multiple criteria in real-time.

Today, we'll break down how this works in 5 minutes."

**[Visual: Logo + Repository name]**

---

## **SECTION 2: THE BIG PICTURE (0:30-1:00)**
*30 seconds*

**[Visual: Flowchart showing Input → Generator → Evaluation → Output]**

**Narration:**
"The model works in a simple pipeline:

**Step 1:** User provides two inputs—how many molecules to generate (1 to 512), and temperature (0 to 2), which controls randomness.

**Step 2:** An LSTM neural network generates SMILES strings—a text notation for molecules, like 'CCO' for ethanol.

**Step 3:** Each molecule is evaluated on four metrics:
- **Validity**: Is it a real molecule?
- **QED**: Is it drug-like?
- **SA**: How hard is it to synthesize?
- **Diversity**: How different is it from others in the batch?

**Step 4:** Results are returned instantly."

**[Visual: Show example output table]**

---

## **SECTION 3: LSTM GENERATOR - THE CORE (1:00-2:15)**
*75 seconds (LONGEST SECTION - MOST IMPORTANT)*

**[Visual: Neural network architecture diagram]**

**Narration:**
"Let's zoom into the generator—the heart of ORGAN-DPP.

It's an LSTM: a recurrent neural network with 2 layers, 512 hidden units, and a 128-dimensional embedding space. Think of it like a chemistry language model, similar to how ChatGPT generates text.

**[Visual: Show SMILES character examples: C, N, O, F, P, S, Cl, Br, brackets, rings]**

It learned chemistry by studying millions of drug molecules. Now it generates new ones character by character."

**[Visual: Animated sequence showing character generation step-by-step]**

**Narration - Temperature Effect:**
"Here's where temperature comes in. It controls how 'creative' the model is:

- **Temperature = 0.7** (conservative): Generates safe, common molecules. Ethanol, benzene, acetone.
- **Temperature = 1.0** (balanced): Mix of typical and novel structures.
- **Temperature = 1.5-2.0** (creative): Experimental, often invalid molecules.

**[Visual: Code snippet showing temperature scaling]**

```python
logits = logits / temperature
probs = softmax(logits)
next_token = sample(probs)
```

**[Explain with visual:]**
Lower temperature makes the probability distribution sharper—the model picks its 'best guess'. Higher temperature flattens it—more randomness.

**[Visual: Bell curves showing narrow vs wide distributions]**

The generator samples up to 120 characters, stopping when it hits the end token or reaches max length."

---

## **SECTION 4: THE FOUR EVALUATION METRICS (2:15-4:00)**
*105 seconds (FAST PACED)*

**Metric 1: VALIDITY (0:15)**

**[Visual: Show RDKit parsing a SMILES string]**

**Narration:**
"Step 1: Validity. We pass the SMILES to RDKit, a chemistry library. It tries to parse it as a real molecule.

If valid ✓ — proceed to next metrics.
If invalid ✗ — QED, SA, and Diversity are NULL."

```python
def validate_smiles(smiles):
    m = Chem.MolFromSmiles(smiles)
    return m is not None
```

---

**Metric 2: QED - Drug-Likeness (0:30)**

**[Visual: Show molecule structure with highlighted properties]**

**Narration:**
"QED = Quantitative Estimate of Drug-likeness. Range: 0 to 1.

The RDKit library computes this in one line:

```python
qed_score = QED.qed(molecule)
```

It analyzes:
- Molecular weight
- Lipophilicity (oil-solubility)
- Hydrogen bond donors/acceptors
- Rotatable bonds
- Ring count

**[Visual: Example molecules with their QED scores]**

- Aspirin: QED = 0.85 ✓ (great drug)
- Random string: QED = 0.21 ✗ (poor drug)"

---

**Metric 3: SA - Synthesis Difficulty (0:30)**

**[Visual: Show formula and example calculation]**

**Narration:**
"SA = Synthetic Accessibility. Range: 1 (easy) to 10 (impossible).

Uses a simple heuristic:

```python
score = 4.0 + (0.1 × ring_count) - (0.02 × heavy_atom_count)
```

**[Visual example:]**
- Simple molecule (ethanol, CCO):
  - Rings: 0
  - Heavy atoms: 2
  - SA = 4.0 + 0 - 0.04 = **3.96** (easy)

- Complex molecule (Aspirin):
  - Rings: 1
  - Heavy atoms: 13
  - SA = 4.0 + 0.1 - 0.26 = **3.84** (moderately easy)

Intuition: More rings = harder. More atoms = easier."

---

**Metric 4: DIVERSITY - The DPP Magic (0:45)**

**[Visual: Show 3 molecules side by side]**

**Narration:**
"This is the innovative part. We don't want a batch of identical molecules. We want diversity.

**Step 1: Morgan Fingerprints**

Each valid molecule is converted to a 2048-bit binary fingerprint. Think of it as molecular DNA encoding the structure.

**[Visual: Show binary vector]**

**Step 2: Gram Matrix**

We compute similarity between all molecules:

```python
X = normalize(fingerprints)
K = X @ X.T  # Gram matrix
```

K[i,j] = how similar molecule i is to molecule j (0 to 1).

**[Visual: Show 3×3 matrix example]**
```
K = [[1.0,  0.7,  0.3],
     [0.7,  1.0,  0.6],
     [0.3,  0.6,  1.0]]
```

**Step 3: Diversity Score**

For each molecule:

```python
diversity[i] = 1.0 - average_similarity[i]
```

**[Visual: Calculate on board]**
- Molecule 0: diversity = 1.0 - (0.7 + 0.3)/3 = **0.67**
- Molecule 1: diversity = 1.0 - (0.7 + 0.6)/3 = **0.57**
- Molecule 2: diversity = 1.0 - (0.3 + 0.6)/3 = **0.70** (most unique!)

Higher diversity = more different from others."

---

## **SECTION 5: COMPLETE PIPELINE & EXAMPLE (4:00-4:45)**
*45 seconds*

**[Visual: Complete flowchart with data at each stage]**

**Narration:**
"Let's trace one batch through the entire system.

**Input:**
- batch_size = 3
- temperature = 0.7

**Generation:**
1. LSTM generates → ['CCO', 'c1ccccc1', 'XXXX']

**Evaluation:**

Molecule 1: CCO (ethanol)
- Validity: ✓ True
- QED: 0.82
- SA: 2.1
- Diversity: 0.45 (among valid molecules)

Molecule 2: c1ccccc1 (benzene)
- Validity: ✓ True
- QED: 0.75
- SA: 3.2
- Diversity: 0.52

Molecule 3: XXXX
- Validity: ✗ False
- QED: NULL
- SA: NULL
- Diversity: NULL (excluded from diversity calc)

**Summary:**
- Total: 3
- Valid: 2

**[Visual: Show JSON output]**"

---

## **SECTION 6: CONCLUSION & KEY TAKEAWAYS (4:45-5:00)**
*15 seconds*

**[Visual: Recap animation]**

**Narration:**
"ORGAN-DPP combines three innovations:

1. **LSTM Generator** - Uses temperature-controlled sampling to generate molecules
2. **Multi-objective Evaluation** - Checks validity, drug-likeness, and synthesis difficulty simultaneously
3. **DPP Diversity** - Ensures molecular variety using fingerprints and Gram matrices

All in under a second. This accelerates drug discovery by enabling researchers to explore millions of candidate molecules automatically.

Thanks for watching!"

**[Visual: Credits with GitHub repo link]**

---

## **PRODUCTION NOTES**

### **Visual Assets Needed:**
1. LSTM architecture diagram
2. Temperature effect visualization (bell curves)
3. SMILES character set
4. RDKit parsing example
5. Molecule structures (ethanol, benzene, aspirin)
6. QED scoring breakdown
7. SA calculation on whiteboard
8. Fingerprint bit vector (2048 bits)
9. Gram matrix 3×3 example
10. Complete pipeline flowchart
11. JSON output sample

### **Color Scheme:**
- Blue: Neural networks
- Green: Valid molecules
- Red: Invalid molecules
- Purple: Diversity metrics

### **Pacing Guide:**
- Intro: Conversational, energetic
- Explanation: Clear, deliberate
- Examples: Point to visuals, pause for numbers
- Conclusion: Inspiring, forward-looking

### **Audio:**
- Background music: Minimal, science-themed
- Voiceover: Clear, professional, slightly conversational
- Transitions: Subtle sound effects (beep for each step)

### **Optional Enhancements:**
- Show real benchmark results
- Demo the API in action
- Compare to other generative models
- Show generated molecule gallery

---

**Word Count: ~1,100 words**
**Read-aloud time: 5:00-5:30 minutes**
**Recommended: Speak at 220 words/minute**
