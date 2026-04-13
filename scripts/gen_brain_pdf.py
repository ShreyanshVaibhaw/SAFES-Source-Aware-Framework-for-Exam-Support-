"""Generate a 4-page Human Brain study notes PDF."""

from fpdf import FPDF
from pathlib import Path

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# ===================== PAGE 1 =====================
pdf.add_page()
pdf.set_font("Helvetica", "B", 22)
pdf.cell(0, 14, "The Human Brain", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Helvetica", "I", 12)
pdf.cell(0, 8, "Comprehensive Study Notes for Exam Preparation", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)

pdf.set_font("Helvetica", "B", 15)
pdf.cell(0, 10, "Chapter 1: Overview and Structure", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "The human brain is the most complex organ in the body, weighing approximately 1.4 kilograms "
    "(about 3 pounds) in an average adult. It contains roughly 86 billion neurons, each forming "
    "thousands of synaptic connections, resulting in an estimated 100 trillion synapses. The brain "
    "consumes about 20% of the body's total energy despite comprising only 2% of body weight.\n\n"
    "The brain is protected by three layers of membranes called meninges: the dura mater (outermost, "
    "tough layer), the arachnoid mater (middle, web-like layer), and the pia mater (innermost, "
    "delicate layer that directly covers the brain surface). Between the arachnoid and pia mater "
    "is the subarachnoid space, filled with cerebrospinal fluid (CSF) that cushions the brain.\n\n"
    "The brain is divided into three major regions:\n"
    "1. The Cerebrum: The largest part, responsible for higher cognitive functions including "
    "thinking, reasoning, memory, language, and voluntary movement. It is divided into left and "
    "right hemispheres connected by the corpus callosum.\n"
    "2. The Cerebellum: Located at the back and below the cerebrum, it coordinates voluntary "
    "movements, balance, posture, and motor learning. It contains more neurons than the rest of "
    "the brain combined.\n"
    "3. The Brainstem: Connects the brain to the spinal cord and controls vital involuntary "
    "functions such as breathing, heart rate, blood pressure, sleep cycles, and digestion.\n\n"
    "The cerebrum's surface is called the cerebral cortex, a 2-4mm thick layer of gray matter "
    "with characteristic folds called gyri (ridges) and sulci (grooves). This folding increases "
    "the surface area to approximately 2,500 square centimeters, allowing more neurons to be "
    "packed into the skull. The cortex contains approximately 16 billion neurons and is "
    "responsible for all conscious thought and action."
))
pdf.ln(3)

pdf.set_font("Helvetica", "B", 15)
pdf.cell(0, 10, "Chapter 2: Lobes of the Cerebrum", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "Each cerebral hemisphere is divided into four lobes, each with specialized functions:\n\n"
    "Frontal Lobe (located at the front of the brain):\n"
    "The frontal lobe is the largest lobe, occupying about one-third of the cerebral cortex. It is "
    "responsible for executive functions including planning, decision-making, problem-solving, "
    "and judgment. The prefrontal cortex, located at the very front, is critical for personality, "
    "social behavior, and impulse control. The primary motor cortex, located along the precentral "
    "gyrus, controls voluntary muscle movements. Broca's area, typically in the left frontal lobe, "
    "is essential for speech production and language processing. Damage to the frontal lobe can "
    "result in personality changes, difficulty with planning, and motor impairments.\n\n"
    "Parietal Lobe (located behind the frontal lobe):\n"
    "The parietal lobe processes sensory information from the body including touch, temperature, "
    "pain, and pressure. The primary somatosensory cortex, located along the postcentral gyrus, "
    "receives tactile information mapped by body region (somatotopic organization). The parietal "
    "lobe also handles spatial awareness, navigation, and mathematical processing. Damage can "
    "cause hemispatial neglect, where patients ignore one side of their visual field."
))

# ===================== PAGE 2 =====================
pdf.add_page()
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "Temporal Lobe (located on the sides of the brain, near the ears):\n"
    "The temporal lobe is primarily responsible for auditory processing. The primary auditory cortex "
    "receives sound signals from the ears. Wernicke's area, typically in the left temporal lobe, "
    "is crucial for language comprehension - understanding spoken and written words. The temporal "
    "lobe also houses the hippocampus, a seahorse-shaped structure essential for forming new "
    "long-term memories and spatial navigation. The amygdala, another temporal lobe structure, "
    "processes emotions, particularly fear and anxiety. Damage to the temporal lobe can cause "
    "difficulties with memory formation (anterograde amnesia), language comprehension (Wernicke's "
    "aphasia), and emotional processing.\n\n"
    "Occipital Lobe (located at the back of the brain):\n"
    "The occipital lobe is the primary visual processing center. The primary visual cortex (V1) "
    "receives raw visual information from the eyes via the optic nerves and lateral geniculate "
    "nucleus. Surrounding association areas (V2, V3, V4, V5) process increasingly complex visual "
    "features: edges, colors, shapes, motion, and object recognition. The ventral stream ('what' "
    "pathway) extends to the temporal lobe for object identification, while the dorsal stream "
    "('where' pathway) extends to the parietal lobe for spatial location and motion detection. "
    "Damage to the occipital lobe can cause cortical blindness, visual agnosia (inability to "
    "recognize objects), or prosopagnosia (inability to recognize faces)."
))
pdf.ln(3)

pdf.set_font("Helvetica", "B", 15)
pdf.cell(0, 10, "Chapter 3: The Neuron and Synaptic Transmission", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "Neurons are the fundamental functional units of the nervous system. A typical neuron consists "
    "of three main parts:\n\n"
    "1. Cell Body (Soma): Contains the nucleus and organelles. It integrates incoming signals "
    "and maintains the cell's metabolic functions. The soma ranges from 4 to 100 micrometers "
    "in diameter.\n\n"
    "2. Dendrites: Branch-like extensions that receive signals from other neurons. A single neuron "
    "can have thousands of dendrites, each covered with dendritic spines that form synaptic "
    "connections. Dendrites conduct electrical impulses toward the cell body.\n\n"
    "3. Axon: A long, thin projection that transmits electrical impulses (action potentials) "
    "away from the cell body to other neurons, muscles, or glands. Axons can range from less "
    "than a millimeter to over one meter in length. Many axons are wrapped in a myelin sheath, "
    "a fatty insulation produced by oligodendrocytes (in the CNS) or Schwann cells (in the PNS). "
    "Myelin increases signal transmission speed from about 2 m/s to 120 m/s through saltatory "
    "conduction, where the action potential jumps between gaps in the myelin called Nodes of Ranvier.\n\n"
    "Synaptic Transmission:\n"
    "When an action potential reaches the axon terminal, it triggers the release of chemical "
    "messengers called neurotransmitters into the synaptic cleft (a 20-40 nanometer gap between "
    "neurons). These neurotransmitters bind to receptors on the postsynaptic neuron, either "
    "exciting it (making it more likely to fire) or inhibiting it (making it less likely to fire).\n\n"
    "Key Neurotransmitters:\n"
    "- Glutamate: The main excitatory neurotransmitter. Involved in learning and memory.\n"
    "- GABA (Gamma-Aminobutyric Acid): The main inhibitory neurotransmitter. Reduces neuronal "
    "excitability and prevents overstimulation.\n"
    "- Dopamine: Regulates reward, motivation, pleasure, and motor control. Deficiency is "
    "linked to Parkinson's disease; excess activity is associated with schizophrenia.\n"
    "- Serotonin: Regulates mood, sleep, appetite, and body temperature. Low levels are "
    "associated with depression and anxiety disorders.\n"
    "- Acetylcholine: Essential for muscle contraction, attention, and memory. Degeneration of "
    "acetylcholine-producing neurons is a hallmark of Alzheimer's disease.\n"
    "- Norepinephrine: Involved in alertness, attention, and the fight-or-flight response."
))

# ===================== PAGE 3 =====================
pdf.add_page()
pdf.set_font("Helvetica", "B", 15)
pdf.cell(0, 10, "Chapter 4: Memory Systems", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "Memory is not stored in a single location but is distributed across multiple brain regions "
    "working together. The brain uses several distinct memory systems:\n\n"
    "Sensory Memory: Holds raw sensory information for milliseconds to seconds. Iconic memory "
    "(visual) lasts about 250 milliseconds; echoic memory (auditory) lasts about 3-4 seconds. "
    "This system acts as a buffer, allowing the brain to select which information to process "
    "further.\n\n"
    "Short-Term Memory (Working Memory): Temporarily holds and manipulates a limited amount of "
    "information (approximately 7 plus or minus 2 items according to Miller's Law) for about "
    "20-30 seconds without rehearsal. The prefrontal cortex is critical for working memory. "
    "Baddeley's model proposes three components: the phonological loop (verbal information), "
    "the visuospatial sketchpad (visual and spatial information), and the central executive "
    "(attention control and coordination).\n\n"
    "Long-Term Memory: Has virtually unlimited capacity and can store information for a lifetime. "
    "It is divided into two major categories:\n\n"
    "A. Explicit (Declarative) Memory - conscious, intentional recall:\n"
    "   - Episodic Memory: Personal experiences and events with contextual details (where, when, "
    "how). Example: remembering your first day of college. Primarily stored in the hippocampus "
    "and medial temporal lobe.\n"
    "   - Semantic Memory: General knowledge, facts, and concepts independent of personal "
    "experience. Example: knowing that Paris is the capital of France. Distributed across the "
    "temporal and frontal cortices.\n\n"
    "B. Implicit (Non-declarative) Memory - unconscious, automatic recall:\n"
    "   - Procedural Memory: Motor skills and learned procedures. Example: riding a bicycle or "
    "typing on a keyboard. Stored in the cerebellum and basal ganglia.\n"
    "   - Classical Conditioning: Learned associations between stimuli. The cerebellum is involved "
    "in simple conditioning; the amygdala handles emotional conditioning.\n"
    "   - Priming: Exposure to a stimulus influences the response to a subsequent stimulus.\n\n"
    "Memory Consolidation: The process of converting short-term memories into stable long-term "
    "memories. The hippocampus plays a crucial role during initial encoding. During sleep, "
    "particularly during slow-wave sleep (SWS) and REM sleep, memories are reactivated and "
    "gradually transferred to the neocortex for permanent storage. This process can take weeks "
    "to years. Emotional memories are consolidated more strongly due to amygdala activation, "
    "which enhances hippocampal encoding through stress hormones like cortisol and norepinephrine."
))

# ===================== PAGE 4 =====================
pdf.add_page()
pdf.set_font("Helvetica", "B", 15)
pdf.cell(0, 10, "Chapter 5: Brain Disorders and Clinical Significance", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 5.5, (
    "Understanding brain structure and function is essential for diagnosing and treating "
    "neurological and psychiatric disorders:\n\n"
    "Alzheimer's Disease: A progressive neurodegenerative disorder characterized by the "
    "accumulation of amyloid-beta plaques and neurofibrillary tangles (tau protein) in the brain. "
    "It begins in the hippocampus and entorhinal cortex, causing memory loss, then spreads to "
    "the cerebral cortex, affecting language, reasoning, and behavior. It is the most common "
    "cause of dementia, affecting approximately 50 million people worldwide. Currently there is "
    "no cure, but medications like cholinesterase inhibitors can temporarily slow symptoms.\n\n"
    "Parkinson's Disease: Caused by the degeneration of dopamine-producing neurons in the "
    "substantia nigra of the midbrain. Symptoms include tremors, rigidity, bradykinesia (slowness "
    "of movement), and postural instability. Treatment includes levodopa (L-DOPA), a dopamine "
    "precursor that crosses the blood-brain barrier, and deep brain stimulation (DBS).\n\n"
    "Stroke: Occurs when blood supply to part of the brain is interrupted (ischemic stroke, 87% "
    "of cases) or when a blood vessel ruptures (hemorrhagic stroke). Neurons begin dying within "
    "minutes of oxygen deprivation. Symptoms depend on the affected area: frontal lobe strokes "
    "cause motor deficits; temporal lobe strokes cause language problems; parietal lobe strokes "
    "cause sensory loss. Rapid treatment with tPA (tissue plasminogen activator) within 4.5 hours "
    "can dissolve clots and reduce brain damage.\n\n"
    "Epilepsy: A neurological disorder characterized by recurrent seizures caused by abnormal, "
    "excessive electrical activity in the brain. Seizures can be focal (originating in one area) "
    "or generalized (involving both hemispheres). The temporal lobe is the most common site of "
    "seizure origin. Treatment includes anti-epileptic drugs (AEDs), and in drug-resistant cases, "
    "surgical removal of the seizure focus.\n\n"
    "Depression: Associated with reduced activity and volume in the prefrontal cortex, hippocampus, "
    "and anterior cingulate cortex, along with dysregulation of serotonin, norepinephrine, and "
    "dopamine neurotransmitter systems. The amygdala shows increased activity, contributing to "
    "heightened negative emotional processing. Treatment includes selective serotonin reuptake "
    "inhibitors (SSRIs), cognitive behavioral therapy (CBT), and in severe cases, electroconvulsive "
    "therapy (ECT).\n\n"
    "Brain Plasticity (Neuroplasticity): The brain's remarkable ability to reorganize itself by "
    "forming new neural connections throughout life. Synaptic plasticity (strengthening or "
    "weakening of synapses) underlies learning and memory. Long-term potentiation (LTP) is the "
    "persistent strengthening of synapses based on recent activity patterns, considered the "
    "cellular basis of learning. Even after injury, the brain can partially compensate by "
    "rerouting functions to undamaged areas. Neurogenesis (the birth of new neurons) occurs in "
    "the hippocampus and olfactory bulb throughout adulthood, though at a much slower rate than "
    "during development."
))

out = Path(__file__).parent.parent / "data" / "uploads" / "Human_Brain_Study_Notes.pdf"
pdf.output(str(out))
print(f"Created: {out.name}")
print(f"Size: {out.stat().st_size // 1024} KB")
print(f"Pages: {pdf.pages_count}")
