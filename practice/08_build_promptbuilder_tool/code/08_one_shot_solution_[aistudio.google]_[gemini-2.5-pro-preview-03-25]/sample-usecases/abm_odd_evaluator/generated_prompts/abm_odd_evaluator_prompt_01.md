
**Objective:** Generate a high-quality TASK_PERFORMING_PROMPT based on the specifications below. This prompt will be used by a human user or another system to instruct an LLM to perform a specific task.

**Your Role (As Renderer):** You are rendering this Jinja template to produce a ready-to-use Task-Performing Prompt for an LLM.

**Core Task for the Final LLM (Defined by User):**
The ultimate task the final LLM needs to perform is:
create high quality scientific evvaluation reports of agent-based models based on their documentation and code



## Assigned Role
You are to adopt the following persona for this task: an expert in agent-based modeling and social simulation, drawing on the principles and best practices outlined in Understanding Complex Systems — Bruce Edmonds & Ruth Meyer (eds.), Simulating Social Complexi
ty: A 
  Handbook.

## Core Task & Context
Your primary task is: create high quality scientific evvaluation reports of agent-based models based on their documentation and code

You MUST perform this task by drawing upon the principles, terminology, style, and information contained within the following provided context. Analyze and utilize this context carefully.

**Provided Context:**
--- START CONTEXT FILE: data/abm_odd_evaluator/context_docs/odd.md ---
Title: The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism

URL Source: https://www.jasss.org/23/2/7.html

Markdown Content:

The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism 
Volker Grimma , Steven F. Railsbackb , Christian E. Vincenotc , Uta Bergerd , Cara Gallaghere , Donald L. DeAngelisf , Bruce Edmondsg , Jiaqi Geh , Jarl Giskei , Jürgen Groeneveldj , Alice S.A. Johnstonk , Alexander Millesa , Jacob Nabe-Nielsene , J. Gareth Polhilll , Viktoriia Radchukm , Marie-Sophie Rohwädern , Richard A. Stillmano , Jan C. Thielep and Daniel Ayllónq

The Overview, Design concepts and Details (ODD) protocol for describing Individual- and Agent-Based Models (ABMs) is now widely accepted and used to document such models in journal articles. As a standardized document for providing a consistent, logical and readable account of the structure and dynamics of ABMs, some research groups also find it useful as a workflow for model design. Even so, there are still limitations to ODD that obstruct its more widespread adoption. Such limitations are discussed and addressed in this paper: the limited availability of guidance on how to use ODD; the length of ODD documents; limitations of ODD for highly complex models; lack of sufficient details of many ODDs to enable reimplementation without access to the model code; and the lack of provision for sections in the document structure covering model design rationale, the model’s underlying narrative, and the means by which the model’s fitness for purpose is evaluated. We document the steps we have taken to provide better guidance on: structuring complex ODDs and an ODD summary for inclusion in a journal article (with full details in supplementary material; Table 1); using ODD to point readers to relevant sections of the model code; update the document structure to include sections on model rationale and evaluation. We also further advocate the need for standard descriptions of simulation experiments and argue that ODD can in principle be used for any type of simulation model. Thereby ODD would provide a lingua franca for simulation modelling.
Keywords: Agent-Based Model, Individual-Based Model, Best Practice, Simulation Model, Standardization, Documentation 
Other articles with these keywords
In JASSS
From Google
Introduction

1.1
Individual- or agent-based models (ABMs in the following) began to be widely applied in ecology in the 1990s and in the social and social-ecological sciences in about 2000 (Vincenot 2018). While mathematical models can be described completely and concisely in the universal language of mathematics, mathematics is neither a complete nor convenient and concise way to capture the important characteristics of simulation models. Consequently, the descriptions of early ABMs were difficult to write and read because no one knew where to place or expect different kinds of information about the model and in what detail. ABM descriptions were often incomplete, so that a complete understanding of the model sufficient enough to allow reimplementation was not possible.

1.2
Incomplete descriptions violate the central requirement of science that materials and methods must be specified in sufficient detail to allow replication of results. Yet ABMs all have common characteristics, which implies that a common language for them could be both useful and feasible. To take advantage of this situation, the ODD protocol (Overview, Design concepts, Details; Grimm et al. (2006); Grimm et al. (2010)) was proposed as a standard format for describing ABMs. The development and adoption of ODD is, in fact, one of several parallel initiatives to overcome the “replication crisis”, which has been recognised in many disciplines as preventing scientists from building efficiently on existing data, methods, experimental designs, and models (Fanelli 2018; Monks et al. 2019; OpenScienceCollaboration 2015; Peng et al. 2011; Wilkinson et al. 2016).

1.3
ODD was designed to make it easier to write and read ABM descriptions and facilitate model replication, while not being overly technical. ODD model descriptions (ODDs, hereafter) can include equations and short algorithms, but are based on written text and intended to be read by humans. They are independent of the hardware and software used to implement the model. ODD consists of seven elements (Figure 1). Conceptually they are divided into the three categories “Overview,” “Design concepts,” and “Details;” hence the acronym ODD. Each of these categories serves a different purpose: giving an overview, explaining how design concepts important for ABMs were used, and explaining all the details of the “machinery” of the model. While these three categories explain the structure of ODD model descriptions, ODD itself is defined by its seven elements.

Figure 1. Structure of model descriptions following the ODD protocol. The protocol itself consists of seven elements, which should be used as given, including the numbering. The categories O (Overview), D (Design concepts), and D (Details) are meant as comments, but not used in ODD model descriptions. There are 11 specific design concepts; if some of them do not apply, they can be left out; if a model includes an important concept of general interest, which is not yet part of ODD, it can be added at the end of the Section 4 'Design concepts'.

1.4
In its first element “1. Purpose and patterns” the purpose of the model and the patterns that serve as model evaluation criteria are briefly described (the new aspect “patterns” is defined below). The element “2. Entities, state variables and scales” lists the different types of entities represented in the model, such as spatial units, agents, and the overall environment. For each entity type, the state variables that characterize it are defined. These are variables that may vary among entities of the same type or vary over time. The temporal and spatial resolution and extent of the model are also specified in this element. The element “3. Process overview and scheduling” provides an overview of the processes in the model: Which entities do what, at what time and in what order, and when are state variables updated? Since this is only an overview, details of these processes are not included here but in the element “7. Submodels”. The element “4. Design concepts” describes how 11 concepts important for the design of ABMs were considered in the model. The final three elements “5. Initialization,” “6. Input data,” and “7. Submodels,” provide detail sufficient for readers to fully understand the model and its rationale and, in principle, completely re-implement it.

1.5
ODD was originally envisioned as a protocol for describing ABMs in ecology, although its authors expressed the hope that it would evolve as its use spread (Grimm et al. 2006). This hoped-for development has certainly occurred in at least two directions. First, ODD has been widely used in fields other than ecology (Section 2). Second, the purpose of ODD has evolved from just describing models to also include improving model design. By requiring modellers to describe all parts of their model, especially the “design concepts” that are unique to ABMs, ODD encourages modellers to also think about, research, explore, and justify all parts of model design (Railsback 2001). Due to these two paths along which ODD and its usage developed, it has contributed not only to standardization of model descriptions but also to the reuse, standardization, and improvement of model designs and modelling concepts.

1.6
In the following section, we briefly list the advantages of using a standard format and the extent to which ODD has been used so far. As the developments in ODD’s purpose have inevitably raised issues and challenges that were not considered when ODD was first created, we next summarize these challenges. Here we first describe all these issues and challenges (Section 3) and then present possible solutions (Section 4). Finally, we provide an outlook on the further development and use of ODD (Section 5). In particular, we propose that most elements of ODD are applicable to any simulation model, not just ABMs, so that ODD could become a “lingua franca” for simulation modelling in general.

ODD’s Benefits and Current Use

2.1
Other standards for reporting on simulation models have been proposed, especially in the area of discrete event simulation (Monks et al. 2019; Wilkinson et al. 2016), but they focus on providing checklists of things that need to be communicated. To our knowledge, none of them have been used for ABMs yet, which may be because discrete event simulation is a mature field that has its own terminology and technique while many ABMs are developed by domain experts with little background in simulation science.

2.2
Because it is used by domain experts from many fields, ODD is less technical and has a strong focus on facilitating communication within and across disciplines. Once a specific communication format has been defined, established and learned, both authors and readers know exactly where to put and expect what kind of information. The benefits of standard formats are particularly obvious for scientific publications, where the introduction, materials and methods, results, and discussion sections serve well-understood purposes and are presented in a particular order. The establishment of such a standard structure for the description of ABMs was the main purpose of ODD (Grimm et al. 2006; Grimm et al. 2010).

2.3
The hierarchical structure of ODD allows the reader to get an overview of the entire model before being asked to consider details. This implies some redundancy but makes reading model descriptions more efficient because readers can decide how much detail they want to go into. The “Design concepts” element provides additional information for understanding why the model was designed as it was. It also serves as a checklist for authors and readers: each of these 11 concepts (Figure 1) affects the scope and utility of the model, so it is important that modellers explicitly consider them. For example, the most important concept details which key processes in the model are imposed via empirical parameters and rules and which arise from adaptive decision-making of the agents. The ability to represent dynamics arising from adaptive decision-making is a primary benefit of ABMs and can make ABMs more flexible and predictive (Grimm & Berger 2016; Railsback 2001; Stillman et al. 2015), but usually it is possible to represent only a few processes this way; selecting them is a critical design decision that should be made carefully and justified clearly.

2.4
After its initial publication (Grimm et al. 2006), ODD was quickly adopted by ecological modellers, so that a first update of ODD and its description, based on its use in more than 50 publications, could be published in 2010 (Grimm et al. 2010). ODD was also introduced to modellers in the social sciences (Polhill 2010; Polhill et al. 2008), presented in several handbook chapters (Grimm 2008; Grimm, Ayllón & Railsback 2017; Grimm & Railsback 2012a; Railsback & Grimm 2012), and used in a textbook (Railsback & Grimm 2019). ODD has also been supplemented with elements to describe ABMs involving human decision making and behaviour (ODD+D; Müller et al. 2013) or describe how data were used in detail to parameterize the ABM (ODD+2D; Laatabi et al. 2018). ODD also became a key component of “TRACE” (TRAnsparent and Comprehensive model Evaludation; Grimm et al. 2014), a standard format for documenting all elements of model development, including parameterization, model analysis, and model “evaludation” (evaluation and validation; Augusiak, Van den Brink, & Grimm 2014).

2.5
The bibliometric analysis of Vincenot (2018) shows that ODD has contributed to the integration of agent-based modelling across disciplines, specifically by linking the disciplines that historically used the terms “individual-based” and “agent-based” and therefore remained separate for many years. Integration was indeed a declared purpose of ODD: once a common language for describing ABMs exists, it becomes easier to learn from each other’s models because it is easier to compare and understand different ABMs, even if they were developed in different disciplines. Moreover, ODD was designed to make model descriptions complete and thereby enable replication, so that submodels describing certain processes or behaviours can more easily be reused in new models.

2.6
ODD is most widely used by ecologists, but its use is also increasing in social (Hauke, Lorscheid, & Meyer 2017) and other sciences (Figure 2; Vincenot 2018). The non-technical nature of ODD facilitates this development: modellers can just use ODD instead of having to create their own documentation format. Moreover, with increasing usage of ODD within each scientific community, more readers, including reviewers and editors, can take advantage of the standardization and will come to expect its use. While ODD has quickly established itself as a widely used format and the absolute number of publications using it has been steadily increasing, its spread has been unequal among scientific domains (Figure 2). The proportion of papers using ODD has grown significantly only in the life sciences and, overall, changes have been slight since 2011.

Figure 2. Annual trends in the use of the ODD protocol were produced on the basis of Scopus searches performed on January 23, 2019. The list of ABM papers was retrieved through the query 'TITLE-ABS-KEY('agent-based model*' OR 'individual-based model*') AND TITLE-ABS-KEY('simulation'))'. These results were crossed with the list of ABM papers citing at least one of the two ODD papers, Grimm et al. (2006, 2010). Post-processing in R was used to group publications by year and by research fields and generate annual usage rate of ODD in the four scientific domains (obtained through aggregation of research field IDs provided by Scopus; as per "Categories" in Supplement S0). In Google Scholar, the 2006 article was cited 2258 times, the 2010 one 1783 (November 6, 2019).

2.7
We do not expect that ODD will ever be used by all modellers and admit that it has limitations for some kinds of models, e.g., discrete-event simulations (Monks et al. 2019). One reason for not using ODD in disciplines other than ecology is obvious: modellers from, e.g., economics, geography, or physics do not usually read ecology journals and therefore may not yet have encountered ODD, or they may perceive it as specifically designed for ecological ABMs. In addition, some scientists simply appear resistant to standardization. However, there are also reasons why the rationale, design, and current use of ODD itself may have prevented its wider use; we address these reasons next.

Issues and Challenges

3.1
Here we briefly list important issues and challenges of ODD that could limit its use. In Section 4 we then suggest possible solutions.

ODD guidance materials are few and not often used

3.2
Inherent to any scientific writing, a factor that limits the wider acceptance and use of ODD is that following an established format without some initial training does not guarantee that the writing is as clear, concise, well-organized, and unambiguous as it could be. However, so far, the guidance material for ODD has been limited to a template provided in the supplement of Grimm et al. (2010), which was not open access and has not been widely used. The guidance provided in the 2010 template is also relatively brief and (now) outdated with respect to the changes in ODD described in Section 4.5.

3.3
The rationale and structure of ODD are simple, so its use should in principle be simple, but comments from users and our experience from reading many ODDs indicate that this is often not the case. Most ODD users report that they initially found it difficult to understand key elements of ODD, especially “state variables” and some of the design concepts. Consequently, many early ODDs have not fully used the protocol as intended, reducing its value for standardization and understanding. The weaknesses and lack of availability of the 2010 template certainly contributed to these problems.

3.4
However, a more fundamental reason for an incomplete or incoherent use of ODD is that modellers tend to describe the mental representation of the model or the narrative of the model rather than the structure and processes of the program that implements the model. These meta-descriptions of mental models are inevitably incomplete; they are simplified versions of our computer models because it is not possible to mentally represent the entire program code. As a result, ODDs are sometimes sloppy, incomplete, and do not provide enough detail to re-implement the model.

3.5
When we think about an ABM, we often focus on its emergent behaviour, but for the ODD we have to describe the low-level processes and interactions from which that behaviour arises. A motto for this issue could be: “Describe what the program does, not what you think the model does”. The lessons from this experience are that the primary ODD learning materials—the template and checklist—need to be more widely available and used, and need to better encourage complete description of what the final model’s computer program does. There certainly is also the need to describe a model's underlying story, or narrative, but ODD is not the place for this (but see Section 4.2 on “TRACE” and 4.3 on “Summary ODDs”).

It is not clear whether the rationale for model design should be explained in ODD

3.6
When ODD was originally conceived, its authors were concerned strictly with the need to describe models accurately and efficiently and did not address the question of whether, and how, an ODD should also describe why each element of a model was designed the way it was. Consequently, some ODDs are strictly descriptive, stating only what the model includes and does, while others are also explanatory, describing the processes and reasoning used to design each element. As ODD has developed into a tool supporting the design of ABMs, the importance of explanation has become obvious. Providing the rationale for model design throughout an ODD can have two major benefits. First, it can greatly increase model credibility by encouraging model developers to think carefully about and test each design decision, and by providing evidence of such careful design to readers and model clients. Second, it can increase the re-use of modelling techniques and theory throughout a discipline by (a) encouraging model developers to look for existing techniques as part of a careful model design process and (b) making it easier for subsequent modellers to know which parts of existing models are suitable for re-use.

3.7
There are several ways that the rationale for model design can be included productively in an ODD. One is simply to provide the basis for all parameter values (e.g., taken from which literature, and why; developed from what data, and how; estimated via calibration, how) and submodels representing processes. Another is to fully implement and analyse each major submodel separately to show that it produces reasonable results under all conditions that can occur in the full ABM. And the “pattern-oriented modelling” strategy discussed in Section 4.23 can provide the rationale for critical design decisions such as what variables and scales are used and how agent behaviours are represented.

3.8
The lesson learned from this experience is that describing the rationale for an ABM’s design in ODD has substantial benefits, although there are likely to be situations in which an ODD should be limited to just model description.

ODDs are often long and must be summarized

3.9
A third factor that appears to limit use of ODD is that ODDs tend to be long for non-trivial ABMs. This is only partly due to the hierarchical structure of ODD, which implies some redundancy, and to the “Design concepts” section, which adds discussion of the model’s underlying rationale that is not absolutely essential for reproducibility. The main reason for this length is that most ABMs are more complex than typical mathematical models, so a model description that contains all the details necessary for replication can easily lead to description that are 5-10 or more pages long. It also simply takes more space to describe an algorithm than to provide an equation. Therefore, ODDs often seem longer than ad hoc model descriptions simply because ODD requires model descriptions to be more complete. ODDs are also less succinct than the specification languages that exist in certain ABM communities (e.g. Z-notation; Wooldridge 2009), which are cryptic to untrained readers. Because ODDs aim to be understandable directly by everybody, they are written in plain English and thus inherently longer than a specialized formalization language with predefined syntax.

3.10
As result of their length, complete ODDs often end up as supplements to journal articles and are not necessarily reviewed or read as often or as carefully. Authors may thus feel that the effort required to write an ODD is not justified, and instead provide only a summary description of their model in the article and, for example, offer their program code on request. This approach is not satisfactory because a full model description is a conditio sine qua non for the use of ABMs as a scientific tool (Grimm et al. 2006; Grimm et al. 2010). A more satisfactory approach would be a complete ODD accompanied by an efficient, standard way to summarize it for journal articles. Until now, there has been no guidance for efficiently producing a summary ODD that is both concise and precise enough for the main text of a journal article. So far there are only ad hoc solutions for such summary ODDs (e.g., Ayllón et al. 2016; Phang et al. 2016; Weiss et al. 2014), which differ widely in structure and depth.

ODD lacks a hierarchical approach for highly complex ABMs

3.11
Most ABMs are of intermediate complexity, leading to ODDs of typically 5-10 pages. However, for some problems and systems, more complex ABMs are being developed. Examples include models of power markets (Li & Tesfatsion 2009), honeybee colonies (Becher et al. 2014), stream fish, (Ayllón et al. 2016; Railsback & Harvey 2002), or harbour porpoises (Nabe-Nielsen et al. 2018; Gallagher et al. 2020). For such models, ODDs are longer than 30-40 pages and often have submodels which by themselves require 10 or more pages. The development of each complex submodel could benefit from its own ODD-like protocol to, e.g., document the patterns used as criteria for evaluating the submodel, the submodel’s entities and processes, and how the design concepts were implemented. However, ODD does not explicitly include or encourage a hierarchical approach in which certain submodels can be described in a format similar to an entire ODD.

Creating a new ODD when re-using parts of a model is inefficient

3.12
Good models are often re-used by creating new versions that are applied to new problems; and experienced modellers often borrow theory or other model components from existing models. In fact, facilitating re-use is a primary motivation for ODD and other standardization efforts. A number of ODD users have therefore encountered the issue of how to prepare an ODD for a new version of an existing model, or for a model that includes parts taken from a previous model. Is it necessary to produce a completely new ODD for each version of a model? Or can we instead prepare a “delta-ODD” that describes only the changes made from the previous version? When we re-use parts of an existing model, can we simply cite its ODD, or should we copy the relevant parts of its ODD, or must we re-create those parts? Re-creating an existing ODD certainly seems inefficient and a potential risk for introducing (but also identifying and correcting) errors.

3.13
While the best way to describe a model modified from one that came with an ODD will depend on the situation, the lesson is that standard guidance on doing so could benefit both authors and journal editors.

ODD still seems ambiguous

3.14
Another reason why some modellers may not use ODD is that they perceive it as too narrative in format to be complete or precise enough to make models reproducible (Amouroux et al. 2010). In part, this perception is due to the characterization of ODD as a “written” format, which could be misinterpreted as “purely verbal”. Of course, all relevant equations and algorithms of a model must be included in an ODD, but even written descriptions with text, pseudo-code, and equations may not contain all the details required for unambiguous replication. Many modellers believe, with good reason, that reading and understanding a model’s computer code is the only completely reliable way to understand what it does. Unfortunately, nothing about ODD so far has facilitated use of the computer code as another, and sometimes essential, way of describing models. Until now, ODD has focused entirely on describing models so completely in text that it is unnecessary to read their code. This focus has been intentional, because a complete model description is essential for tasks including software testing and because computer code can be at least as difficult to understand as a written description. But links between ODD and code could provide a lifeline for readers determined to fully understand exactly how a model works when the written description is ambiguous.

3.15
Interestingly, there is also a contrary view on narrative model descriptions because different disciplines have different communication cultures. While ODD can be considered too narrative or verbal in the natural sciences, the opposite can be the case in the social sciences. In social sciences, more than in natural sciences, there is typically a narrative that runs through each model element (the choice of agents, processes, model purpose, parameters, etc.). Social science modellers often construct their models from this narrative, and through this narrative they communicate their models to the readers. ODD with its separate sections can make it difficult for the reader to see the common thread, i.e., the story that connects them all. This challenge reflects a fundamental difference between natural sciences and sociology in particular, the former being based on the notion of entities and variables, while the latter is based on the notion of discourse and communication. While ODD originated in the natural sciences style, there are ways that it can better present a model as a narrative, and doing so could make the ODD more effective and the model more understandable.

3.16
The lesson is: the extent to which ODDs should be narrative vs. mathematical and technical can vary among disciplines, and ideally ODD can accommodate this variation. One obvious way to meet ODD’s goal of providing complete description even in more narrative descriptions is to help readers find the computer code implementing each part of the model.

ODD is not clearly linked to pattern-oriented modelling and does not describe criteria for a model being fit for its purpose

3.17
As discussed in Section 1, ODD has developed into a valuable tool for designing ABMs; but it is not the only such tool. “Pattern-oriented modelling” (POM; Grimm & Railsback 2012b; Grimm et al. 2005; Railsback & Grimm 2019) is a strategy for basing the design, evaluation, and parameterization of ABMs on patterns observed in the real system addressed by the model. In brief, POM involves identifying observed patterns that characterize the model system with respect to the model purpose, i.e. are driven by the mechanisms, occur at the scales, etc., believed important for the model purpose. Once the patterns are identified, POM then consists of (a) selecting model entities, state variables, and scales so that the patterns could be reproduced; (b) testing “theory” for agent behaviours by showing whether alternative submodels for behaviour cause the patterns to emerge from the model; and (c) using quantitative patterns to identify useful parameter values (Wiegand et al. 2003). Railsback & Johnson (2011, 2014) provide a particularly explicit example of POM.

3.18
Presumably because it addresses three of the biggest challenges in agent-based modelling (How do I find the right level of detail? How do I model agent behaviour? How do I estimate parameter values?), POM appears to have become widely used. Vincenot (2018) determined that the primary publication on POM (Grimm et al. 2005) is, like the papers describing ODD, among six “fusion papers” that contributed most to unification of agent-based modelling across disciplines. Even when POM is not used explicitly, observed patterns are almost always important in model design. Very often, the purpose of an ABM is to explain patterns observed in reality, so these patterns are important criteria for whether the model is useful. The simplest toy ABMs that do not pretend to represent specific real systems are still based on general patterns observed in reality; very common examples include equilibrium population dynamics, segregation in cities, and flocking in birds. Identifying such patterns explicitly in the ODD helps its authors answer important questions such as: Why was the model designed as it was? What criteria were or could be used to determine whether a model is suitable for the stated purpose?

3.19
However, integrating POM with ODD, such as by describing in an ODD what patterns were used in what ways to design the model, has proven frustrating: there is no specific place in ODD for emergent patterns, and it is not obvious where they should be described. The element “Design concepts/Theoretical and empirical background” of ODD+D (Müller et al. 2013) includes references to patterns, but we suggest to make this link more prominent by referring to them early on in an ODD. Moreover, because the same observed patterns are used in multiple ways, it seems efficient to describe them early in an ODD so they can simply be cited as needed in later sections. The lesson is that ODD needs a place to describe the patterns used to design and evaluate a model, and that place should be before describing things like entities and state variables that may be chosen using the patterns as a basis.

Improving Clarity, Replication, and Structural Realism with ODD

4.1
This section describes the proposed solutions to the issues and challenges identified in Section 3. In some cases, solutions have been implemented in revisions to ODD and updates to its supplements, especially a completely revised ODD guidance and checklist. Table 1 includes an overview of all supplements, which illustrate or exemplify our suggestions for how to address the issues identified in Section 3.

Table 1: Overview of supplements to this article
Supplement	Purpose and content
S1: ODD Guidance and checklists	For each ODD element, and for each Design concept, the rationale, specific guidance, and checklists are provided. Examples from existing ODDs are included.
S2: Summary ODD	A template is provided for writing summary ODDs which, in the main text of an article or report, summarize, in a more narrative way, the essential features of the ODD model description while using ODD keywords. Examples are included.
S3: Nested ODD	Guidance and examples are given for writing nested ODDs where the description of highly complex submodels by itself follows a slightly reduced ODD protocol.
S4: ODD of modified models	Guidance and examples are given for writing ODDs of models which largely build on earlier models and, hence, their ODDs.
S5: License agreement for ODD	For ODD of modified models (S4) it needs to be clear whether we are allowed to use, verbatim, earlier ODDs or parts therefore. Here, guidance is given on how to explicitly declare the conditions under which ODDs can be re-used by others. Examples are provided.
S6: Example TRACE documents	TRACE (TRAnsparent and Comprehensive model Evaludation) is a standard format for planning and documenting all elements of iterative model development, analysis, and application (Grimm et al. 2014). Here, two examples TRACE documents are given (Ayllón et al. 2016; Nabe-Nielsen et al. 2018).
S7: Describing simulation experiments	Guidance and examples are given on how the “Simulation experiments” part in the “Materials and Methods” section of an article can be organized and how the experiments can be described. This guidance also covers calibration and model analysis.
ODD learning materials and guidance

4.2
To address the issues described in Section 3.1, we thoroughly updated the ODD learning materials (Supplement S1). For each ODD element the learning material provides an (1) overview explaining the scope and rationale of this element, (2) explicit guidance, e.g. “Do not confuse parameters with state variables” and corresponding explanations, and (3) short examples taken from existing ODDs. These examples are for illustrative purposes only, so they should not be copied but used as guidance. Separate guidance and checklists are provided for each of the design concepts of ODD’s element “5. Design concepts”. As an example for the structure and content of the guidance provided in Supplement 1, Box 1 presents the overview, guidance, and checklist for the ODD element “1. Pattern and purpose”.

Box 1: Example from Supplement S1, which provides the overall rationale, guidance, checklists and examples for each of the seven ODD elements, including additional guidance and examples for all 11 Design concepts.
1. Purpose and patterns
Every model has to start from a clear question, problem, or hypothesis; readers cannot understand your model unless they understand its purpose. Therefore, ODD starts with a concise and specific statement of the purpose(s) for which the model was developed. The examples of Element 1 we provide below categorize model purposes into types of general purpose (e.g., prediction, explanation, description, theoretical exposition, illustration, analogy, and social learning). It is useful to first identify one or more of these general types of model purpose before stating the specific purpose.
The “patterns” part of this element is new in this version of ODD. It helps clarify the model purpose by specifying the criteria you will use to decide when your model is realistic enough to be useful for its purpose. The patterns are observations, at the individual or system level, that are believed to be driven by the same processes, variables, etc. that are important for the model’s purpose. For some of the possible purposes, the model will be assumed useful only if it can reproduce the patterns. For other purposes, not reproducing the patterns can be an important result because it indicates that some mechanism is missing or inadequately represented. These patterns can be observations from the real system being modeled, obtained from data or literature. For models not based on a specific real system, the patterns are often general beliefs about how the system and its agents should behave. Including patterns in ODD is also a way to link it explicitly to “pattern-oriented modeling”, a set of strategies for designing and evaluating ABMs; this link is explained in the main text of this article and by Railsback & Grimm (2019)
Guidance
Make the purpose specific, addressing a clear question.
The purpose statement should be specific enough to enable a reader to independently judge a model’s success at achieving this purpose as well as to serve as the primary “filter” for what is and is not in the model: ideally the model should only include entities and mechanisms that are necessary to meet its purpose. If the purpose statement is only general and unspecific, and especially if it lacks patterns for evaluating the model’s usefulness, then it will be difficult to justify (and make) model design decisions.
Some ODDs state only that the model’s purpose is to “explore,” “investigate,” or “study” some system or phenomenon, which is not specific enough to assess the model or to determine what the model needs to contain. An imprecise purpose such as this is often an indication that the modeler simply assembled some mechanisms in an ABM and explored its results. Studies like this can be made more scientific by stating the purpose as a clear question such as “To test whether the mechanisms A, B, and C can explain the observed phenomena X, Y, and Z.”
Include the higher-level purpose.
The purpose statement should also clarify the model’s higher-level purpose: whether it is to develop understanding of the system, or to make specific predictions, etc. Different high-level purposes lead to different model designs. Use the general purposes from the examples of Element 1 we provide below as a guide.
Tie the purpose to the study’s primary results.
One way to make this statement of model purpose specific enough is to explicitly consider what point you are trying to demonstrate with the model. The statement should allow the readers to clearly judge the extent to which the model is successful. This is closely related to the primary analysis you will conduct with the model. Think about the key graph(s) you will produce in your “Results” section, where you apply the model to your main research question. The model’s purpose should include producing the relationship shown in this graph.
Define your terms.
If you state that your model’s purpose is (for example) to “predict how the vulnerability of a community to flooding depends on public policy”, you still have not stated a clear model purpose. The term “vulnerability to flooding” could mean many things: drowning, travel delays, property damage, etc.; and “public policy” could refer to zoning, insurance, or emergency response. Be clear about exactly what inputs and results your model addresses.
Be specific to this version of the model.
To keep the description clear and focused, do not discuss potential future modifications of the model to new purposes or patterns. (Future plans might be described instead in the Discussion section of a publication.) However, if the same model is designed for multiple purposes, those purposes should be described even if they are not addressed in the current publication.
Do not describe the model yet. Authors are often tempted to start describing how the model works here in the purpose statement, which is a mistake. Instead, address only the purpose here and then, in subsequent sections, you can tie the model’s design to the purpose by explaining why specific design decisions were necessary for the model’s purpose.
Make this purpose statement independent.
Model descriptions are typically published in research articles or reports that also include, in their introduction, a statement of the study’s purpose. This ODD element should be independent of any presentation of study purpose elsewhere in the same document, for several reasons: (a) an ODD model description should always be complete and understandable by itself, and (b) re-stating the model purpose as specifically as possible always helps modelers (and readers) clarify what should be in the model.
Use qualitative but testable patterns.
Patterns useful for designing and evaluating ABMs are often general (observed at multiple locations or times) and qualitative. However, using patterns to evaluate a model requires that they be testable: you need a reproducible way to determine whether the model matches the pattern. Making patterns testable can be as simple as stating them as qualitative trends, e.g., that output X increases as variable A decreases. We generally discourage statistical definitions of patterns where the pattern is, in fact, qualitative. There are more appropriate ways of formalizing qualitative patterns, e.g. Thorngate & Edmonds 2013).
Document the patterns.
A complete description of the patterns used in modelling needs to document why the patterns were selected: what evidence supports them, and what is their role in justifying the purpose? Documenting patterns can range from simply stating them as widespread (or your own) beliefs, to citing multiple empirical studies that observed each pattern. Thorough documentation of several patterns can require substantial text, which could conflict with keeping this “Overview” part of ODD short. In this case, patterns can be thoroughly documented in a separate section of a report or article and summarized in the ODD model description; thorough documentation of the patterns in the ODD description is not essential for it to be complete enough to make the model reproducible.
Checklist
The ODD text for this element should describe:

- The model’s specific purpose(s).
- The patterns used as criteria for evaluating the model’s suitability for its purpose.
Element 1 examples
Purpose statements
Pattern descriptions
Inclusion of rationale

4.3
Section 3.2 discusses the benefits of including in an ODD information about what model design decisions have been made and why. We can envision circumstances in which users may decide to restrict an ODD to only description and not rationale, e.g., in the user documentation of a widely used model or when describing a model developed by someone else, e.g., those in the NetLogo models library (Wilensky 1999). However, in our new guidance we now explicitly encourage discussion of the rationale behind each ODD element. Each ODD element includes the optional subsection “Rationale” where information about why a certain model design was chosen can be provided to add credibility to the model’s design and help readers to better understand, and possibly re-use, the model design.

4.4
Including the rationale for model design can often substantially increase the length of an ODD: it can take many pages to explain the literature review, data analysis, analysis of alternative approaches, etc., that lead to a model design decision. The following subsection addresses ways to deal with problems caused by ODD length. An alternative, but not mutually exclusive, way to document the rationale underlying a model is to produce a TRACE document, which includes justifications of all major elements of a model’s design (Augusiak et al. 2014; Grimm et al. 2014). Two example TRACE documents are provided in Supplement S6.

Summarizing ODDs

4.5
Section 3.3 identifies the length of many ODDs as a challenge because often only a summary can be included in the main text of a publication. Including the rationales for model design as recommended in Section 4.2 can aggravate this problem by making ODDs considerably longer. We can provide some guidance, from our experience, for producing summary ODDs suitable for the main text of journal publications. This process introduces more of the narrative style of the social sciences (Section 3.5) to enhance overall comprehension of a model, with detail intentionally relegated to the full ODD.

4.6
The purpose of a summary ODD is to provide a narrative description of the entire model and at the same time be specific enough that the main results of the model can be understood without necessarily resorting to the full ODD model description. We recommend always writing a full ODD first, whether it can be included in the main text of a document or needs to be included in the supplement.

4.7
The summary should start with the three overview elements (Figure 1) brought into a more narrative, story-like form. Section titles should be omitted and long lists of state variables moved to tables. Entities can, if this improves the narrative, be described together with the processes they execute. However, to help readers find further details in the full ODD model description, keywords from ODD should be used and italicized, in particular: purpose, entities, state variables, scales, processes, schedule, design concept, initialization, and submodel. The only design concepts and submodels that should be presented in some detail are those essential to understanding the main idea of the model and the application addressed by the publication. The ODD elements “initialization” and “input data” should be briefly described if they are essential, e.g., if scenarios with different initial conditions are implemented or if input data are essential drivers of model dynamics. If external drivers are key elements of the question addressed with the model, for example when exploring effects of climate change, it should be said here where in the model and how their effects are represented.

4.8
If the resulting summary model description still does not fully capture the overall narrative of the model, which might be the case for certain model purposes and within certain areas (social sciences), the overall narrative of the model might be presented first, without reference to the terminology and structure of ODD, but then the summary ODD and a link to the full ODD should follow. In any case, it would be worthwhile considering a graphical representation of the model’s ODD; an example of such a “visual ODD” is provided in Figure 3.

Figure 3. Example visualization of what a model is and does, based on ODD. The figure provides an overview of the entities and how they are initialized (“Initialization”), of the processes and their scheduling (“Submodels”), and of the observation, i.e. the key model output that is used for addressing the question of the model (“Analyses”); from: Milles et al. 2020).

4.9
General advice for describing models through narratives is the same as for scientific writing in general, where the context is provided first before presenting something new (Gopen & Swan 1990). In Supplement S2, we provide a template for writing summary ODDs, and examples of summary ODDs.

Hierarchical ODDs of highly complex models

4.10
If an ABM includes submodels which by themselves require 10 or more pages of description, we recommend writing “nested ODDs”: the submodel is described largely in the same way a full ABM is described, by its own, slightly reduced, ODD which should include the Section 1 “Purpose and patterns”, Section 2 “Process overview and scheduling”, and Section 7 “Submodels”. The other ODD elements, “Entities, state variables, and scales”, “Design concepts”, “Initialization”, and “Input data” should still refer to the entire model, not to specific submodels.

4.11
Further means for keeping ODDs of highly complex models readable and useful are: (1) group parameters according to the submodels in which they are used rather than providing a single large table of model parameters, which are otherwise presented at the beginning of the “Submodels” element; and (2), if numerous equations are used, summarize these in tables and explain the rationale of each equation in the text. This disentangling of equations and text is more concise, provides a better overview, and is easier to read and understand (e.g., ODD of Galic et al. 2018). In Supplement S3, we provide an example of a nested ODD (Gallagher et al. 2020).

Developing ODDs when re-using parts of existing models

4.12
How can modellers develop an ODD efficiently when parts of the model are re-used from other models or when producing a new version of an existing model? How can existing ODDs be re-used? Our recommendations depend on the exact situation.

4.13
It is certainly efficient to describe a new version of an existing model by preparing a “delta-ODD” that describes only the parts of the model that have been changed. The “delta-ODD” identifies the ODD elements that have changed and provides new description for those elements; examples are given throughout the textbook of Railsback & Grimm (2019) and in Railsback & Harvey (2020). However, this approach is appropriate only when the ODD of the original model is readily available to anyone attempting to use the delta-ODD, for example by being re-published as a supplement or freely available on the Internet with a link provided in the delta-ODD.

4.14
Our experience has been that the “delta-ODD” approach is often not appropriate or feasible because: the original ODD is not freely and easily available, or a journal expects model-based publications to include complete, stand-alone model descriptions, or the new model includes only part of the previous model, with many new parts. Therefore, we often need to prepare a new, complete ODD for a model that is partly, or largely, the same as a previously described model. Making it efficient to prepare such ODDs is important for encouraging standardization and re-use of models and model components.

4.15
The most efficient way to prepare a new, complete ODD based in part on a previous model is simply to copy the relevant parts of the previous model’s ODD, giving full credit to the original authors and making it clear which work is theirs. Supplement S4 includes an ODD of a model that was adopted and modified two times, by slightly different teams of authors (Johnston et al. 2014; Johnston et al. 2015; Johnston, Sibly, & Thorbek 2018); a further ODD of a modified model is presented in Supplement S3.

4.16
To do so of course requires that copyright issues be clarified, and there are steps that authors can take to make their ODDs easier for others to re-use. Copyright concerns apply to ODDs published in open access repositories as well as to those published as supplements to proprietary journals. For most journals, supplements are not subject to the copyright of the journal as long as the journal has not invested in them via their layout or any other way, so their copyright remains with the author. Therefore, authors of ODDs published as supplements to journal articles can, at the time of publication, give permission for others to later re-use parts of the ODDs, but they should carefully check the journal’s Copyright Transfer Agreement before they do so.

4.17
We recommend that ODD authors add a license, e.g. in a footnote that sets out the terms of use of the ODD in the same way that terms of use should be stated for the model’s software. This license should include a “copyleft” statement which requires that future users of an ODD or parts of it do not restrict its use by their own license statements. Standard licenses are widely used in open software communities, for example GNU or more generally UNIX developers (one common software licence is discussed at: https://www.gnu.org/licenses/fdl-1.3.en.html). They allow others to build on existing work and reuse ODD text while providing full credit to the original work through references. Some of these licenses also include a disclaimer of liability, (i.e. “no warranty” disclaimer, e.g. clause 5 of the CC-BY-SA), which protects the creator against legal action in case the ODD does not perform as expected. In Supplement S5, we provide an example license and links to additional licensing information, but each author must make their own decision on whether and how to allow re-use of ODDs and software. For example, you might want to restrict the license to the factual parts of the ODD, but not to the narrative ones.

4.18
When preparing an ODD based on that of an existing model, it is critical to clearly indicate that the ODD includes material from a previous one, give full credit to original authors, clearly distinguish the re-used from original work (e.g., by setting new and deleted text in different fonts or colours), and ensure that the new ODD is published under terms that do not violate the original material’s license (reciprocity requirement especially).

Reducing ambiguity by linking ODD to code

4.19
To many simulation scientists, a model’s computer code is its most authoritative and unambiguous description. Therefore, providing clear links between ODD and the computer code can make a model seem more transparent and its description less ambiguous. If readers can easily find and read the code that implements any part of an ODD, they are more likely to thoroughly understand and even replicate the model. Most programming languages are relatively similar and seem understandable over the few lines typically needed to code ABM algorithms or submodels, so even readers unfamiliar with a language can try to understand an algorithm from its code and check whether it matches the ODD narrative. Here, we recommend ways to provide such links, which first requires making a model’s code (appropriately licensed and copyrighted) available with its ODD. Most journals do not require code to be made available but doing so is widely considered good scientific practice in line with current trends towards open science.

4.20
There are well-known limitations of publishing model code. Teams that have invested years in the development of complex models certainly want to benefit from this investment before others do; however, code for key algorithms and data structures could be provided instead of the full program. Furthermore, a model’s code itself is not always sufficient for understanding exactly how it executes; information may also be required about the compiler or interpreter, code libraries, any numerical solution methods (Seppelt & Richter 2005), and even the hardware and operating system. Therefore, we recommend that at least revision numbers of external software/library, architecture (e.g. x86, 32/64 bits) and operating system version always be provided. Further, computer code can be misinterpreted, and important software details can be specified in places other than the code statements; especially, the popular NetLogo platform provides many extremely useful primitives that must be fully understood (almost always possible from their documentation) to understand a model code.

4.21
One way to link ODD descriptions to computer code is simply through careful naming conventions. Using the same names for variables, parameters, and submodels in both ODD and code makes it easier to find the code implementing specific parts of a model. Similarly, code comments can be used to identify where specific ODD elements, algorithms, or even numbered equations, are programmed.

4.22
Links between ODD and code can also be more comprehensive and specific. Becher et al. (2014) provided both the ODD model description and the computer code for their complex model of honey bee colonies, BEEHAVE, in a single file that includes hyperlinks from the ODD to the corresponding code. Another potential approach is to add notes or a table to the ODD to identify the code locations (file, procedure or function name, or even line number) where each ODD element, submodel, or algorithm is implemented.

Linking ODD to pattern-oriented modelling

4.23
In Section 3.7, we identified the important benefits and popularity of POM as another important tool, alongside ODD, for designing ABMs and documenting their validity and credibility. We also identified the problem that there has not yet been a specific place in ODD where the observed patterns used in POM should be stated. We therefore supplement the ODD element “1. Purpose and patterns” to explicitly include the patterns that are used in POM to design and evaluate the ABM or otherwise serve as criteria for whether the model is realistic enough for its intended purpose. The first ODD element was chosen as the location where these patterns are stated for two key reasons. The patterns can be used, via POM, to select the entities, state variables, and scales of a model, so the patterns need to be identified before these components of model structure are described and justified in ODD element 2. The patterns are identified with the model’s purpose because purpose and patterns are tightly linked: explaining the patterns is often part of the model’s purpose, and we use the patterns to determine whether the model is suitable for its purpose. Furthermore, in the new ODD guidance we recommend that the overall purpose of the model be explained in more detail, as different purposes imply different criteria for the design and evaluation of a model. In addition to the specific purposes of a model, it is also helpful to clearly state the general type(s) of the model’s purpose. General types of model purpose can be described in broad categories such as understanding/explanation, prediction, and demonstration of ideas (Roughgarden et al. 1996), but there are also more refined categories, which strongly affect how a model is designed, analysed, and to be evaluated (Edmonds et al. 2019). These more specific categories seem to be most relevant in social sciences where models are often used to illustrate narratives rather than to represent a specific, empirical system.

4.24
Examples of this new “1. Purpose and patterns” ODD element are provided by Railsback & Grimm (2019); this textbook includes patterns in the first ODD element for seven ABMs. These examples include some very simple models, not specifically related to any real system, for which observed patterns were nonetheless important in establishing the model’s purpose. One important caveat with POM is the need to also report patterns observed in reality that were considered essential prior to model development, but which the model consistently failed to reproduce. Reporting, in the first ODD element, only those patterns that the model could capture would resemble “HARKing” (Hypothesizing After Results are Known). Better practice would be to report on missing patterns, which would indicate that important processes were not yet identified, or understood. Such reporting would prime the reader for topics that will likely be covered in the discussion, promoting readability of the article as a whole.

Outlook

5.1
Here we outline possible future developments and applications of ODD. Each would require careful consideration and testing by the modelling community. We hope that these and other ideas to increase the usefulness of ODD and related approaches will be pursued not only by ourselves, but by the entire modelling community.

ODD for non-agent-based simulation models

5.2
Only a few parts of the ODD protocol apply specifically to ABMs. Those parts are all in the “5. Design concepts” element, especially emergence (of behaviour), adaptation, objectives, learning, prediction, sensing, and collectives. Other ODD elements are relevant to any simulation model. Thus, it seems possible to describe any simulation model with ODD.

5.3
ODD has in fact already been used for models that are not ABMs. For example, Meli et al. (2014), Radchuk et al. (2014) and Erickson et al. (2016) used ODD to describe matrix models, and Erickson et al. (2017) for an integral projection model. Müller et al. (2007) used ODD to describe an ecological-economic model of pastoral-nomadic range management that is not agent-based and employs difference equations as submodels. Lamonica et al. (2016) similarly used ODD to describe a model that is fully based on ordinary differential equations.

5.4
Besides these, ODD has also been used to document hybrid models (Vincenot, Mazzoleni, & Parrott 2016) in which ABMs integrate other modelling approaches. For instance, DEB-IBM (Martin et al. 2013; Martin et al. 2012) is an ABM of water fleas (Daphnia) in which the energy budget of individuals is modelled using Dynamic Energy Budget theory (DEB; Kooijman 2010), which is formulated via ordinary differential equations. Similarly, ODDs were produced for several System Dynamics (SD)–Individual-based (IB) hybrid models, which took advantage of SD stock-and-flow modelling to render continuous processes in ABMs and visualize feedback loops. This approach was used to explain spatio-temporal patterns in plant communities (Vincenot et al. 2017; Vincenot et al. 2016), reconstruct cell-based morphogenesis mechanisms (Hay Mele et al. 2015), render memory effects in spatial resource use by foragers (Vincenot et al. 2015), study the effect of population structure on epidemic resurgence (Vincenot & Moriya 2011), and simulate lake restoration scenarios (Martin & Schlüter 2015). Large hybrid models often couple existing mathematical models of environmental systems with ABMs or other simulation models of the human component, e.g., combining models from hydrology, vegetation science, and social science to address land use change (Drogoul, Huynh, & Truong 2016; Janssen et al. 2011). In this context, hybrid models are increasingly used to address the feedbacks among environmental compartments that can no longer be ignored in times of rapid global and regional change (Ayllón et al. 2018).

5.5
All the foregoing models formulated based on differential equations or algorithms (e.g. decision trees) or both were relatively seamlessly integrated into ODDs describing complete models. Because simulation modelling in general is much more mature than agent-based modelling, its existing literature on model reporting (e.g., Monks et al. 2019) should be considered in adapting ODD to non-ABM simulation models. ODD already appears useful in its current form in the particular case of hybrid agent-based models (or more generally modular models coupling interacting self-standing submodels), but experience may identify modifications or supplements to ODD to improve its value for these increasingly important models. We can already recommend adding a subsection in the ODD element “Submodels” to describe under which framework submodels were coupled, how and when they interact, and which the particular variables and processes are through which data exchange and synchronization takes place (“hooks” between the submodels; see for example appendix 1 in Vincenot et al. (2017).

ODD and description of simulation experiments

5.6
An ODD corresponds to the “Materials” part of the Materials and Methods section of a scientific publication because it describes the virtual laboratory in which we conduct simulation experiments. The “Methods” equivalent then must describe how we used the materials—the model—in simulation experiments. Previous publications on ODD recommended that an ODD be followed by a section entitled “Simulation Experiments” but provided no further guidance.

5.7
We debated expanding ODD to include a protocol for describing simulation experiments but chose not to do so. A protocol for describing simulation experiments could be used by authors as a checklist to ensure that important elements of model calibration and analysis are documented, and readers would know where to expect what kind of information, just as with ODD. However, standardizing the description of simulation experiments could be just as complex as ODD currently is, and deserves separate, in-depth consideration (see, e.g., the recommendations of Waltemath et al. 2011). Moreover, designing and describing simulation experiments is a separate task from designing and describing a model: the same model can be used for different simulation experiments, and the same experiments are sometimes executed using different models.

5.8
TRACE documents (Augusiak, Van den Brink, & Grimm 2014; Grimm et al. 2014; Schmolke et al. 2010) already provide a comprehensive format for documenting all relevant elements of model development, testing, and use. Example TRACE documents of Ayllón et al. (2016) and Nabe-Nielsen et al. (2018) are in Supplement S6, and further examples can be found in the supplements to Courbaud et al. (2015), Dey et al. (2017), Erickson et al. (2016) and Weller et al. (2016). TRACE, though, is a format for supplements, not for the main text. What might be needed is a format corresponding to TRACE but which is suitable for main texts. While we cannot provide a full-fledged solution here, in the Supplement S7 we provide a possible template; its elements are adopted from TRACE, and they are explained in detail in Grimm et al. (2014).

Automated links between ODD and code

5.9
Model development should always be a process that begins with written documentation that is carefully discussed, reviewed and revised; then, at some point, the model design must be “frozen” and implemented in a computer program, with the written description updated as software development identifies mistakes and ambiguities. Automated links between written description and software are naturally an ideal—some or all of the software could be produced from the written description and perhaps the description could be updated automatically when code is modified. We are unaware of active efforts to produce such links between ODD and ABM software, but technically, it seems possible to write ODDs in such a way that they can be automatically converted into the backbone of the corresponding computer code. ABM is a direct form of object-oriented formalization, and thus related models are mostly implemented using object-oriented programming (OOP). This property is visible in ODD’s descriptive structure, in which for instance “entities”, “state variables/attributes” and “processes” are clear equivalents to OOP classes, attributes and methods. As a result, the standardized list of entities, attributes and processes of an ODD could be used to generate their counterpart in OOP code skeletons (e.g. Java classes). Similar automated processes already exist for many OOP languages in the case of UML to code conversion.

5.10
Several cautions are in order in pursuing the goal of linking ODD and code. First, care must be taken that ODD is still written for people, not computers. Only verbal, non-technical descriptions of a model force us to try to understand what a model is, how it works, and why it was designed in a certain way. For example, markup languages can be read by people but their main purpose is to be read by computers, which means they do not sufficiently force us to think about the model. Second, our experience with several ABM platforms that attempted to partially automate development, e.g., by providing graphical tools for outlining software, were that these were useful mainly for tasks that are relatively easy anyway and did not eliminate the more challenging tasks of coding each model’s unique details. Third, the semantic links between classes in object-oriented programming and everyday meanings in natural language are not as trivial or straightforward as may at first appear to the naïve programmer (LaLonde & Pugh 1991; Polhill 2015; Polhill & Gotts 2009).The code template produced from the model’s design is thus not necessarily the best (most efficient and/or readable) way to implement the software.

5.11
Fourth, the practice of preparing and ‘locking off’ design documentation prior to implementation in code echoes the rather out-dated ‘waterfall’ approach to software engineering (Adenowo & Adenowo 2013). This might work fine in mono-disciplinary or similar contexts where there is a small team of people with similar expertise; it will be less suitable in inter- and especially transdisciplinary contexts, where more iterative and ‘agile’[1] approaches to software development are generally seen as more effective (e.g. Étienne 2013; Moyo et al. 2015).

5.12
Another option worth considering for ODD is “literate programming” (Knuth 1984) where “programs are written as an uninterrupted exposition of logic in an ordinary human language, much like the text of an essay, in which macros are included to hide abstractions and traditional source code.”[2]

Organizing ODD’s maintenance and development

5.13
So far, the use of ODD as the standard format for describing ABMs has been promoted by a small but diverse group of experienced modellers. The original ODD publication (Grimm et al. 2006) asked users to cite it, which allowed us to monitor how coherently and efficiently ODD was used and therefore produce the 2010 update and this article.

5.14
One long-term issue for ODD is who will continue to maintain and update it. Although ODD is used in a textbook (Railsback & Grimm 2019), recommended by the CoMSES/OpenABM network (https://www.comses.net/), and some journals (e.g. JASSS, Ecological Modelling), it is worth considering alternative ways to organize the maintenance and development of ODD and related standards. Existing networks, such as CoMSES, might be appropriate if they are not domain-specific.

5.15
A second issue is monitoring and promoting the quality of ODD applications. One way to improve the coherent use of ODD could be by allowing ODDs to be reviewed and certified by users who have undergone training and produced high-quality ODDs themselves. “Official” ODD certifiers could be qualified by, e.g., attending one-day courses, submitting their own ODDs, and being “examined” by reviewing test ODDs (for example in a quality check process similar to what is implemented in CRAN; Hornik 2012).

Discussion

6.1
ODD has been used much more widely than anticipated by its original developers, which indicates that a standard format for describing ABMs, and possibly other simulation models, is needed and useful. The initial success of ODD convinces us that it should be used even more, and more coherently, in the future. ODD is a positive-feedback technology: the more it is used, the more valuable it is to its users and scientific communities. ODD has already contributed to unifying agent-based science by connecting the previously separate bodies of literature that used the terms “agent-based” and “individual-based” (Vincenot 2018). Further benefits include facilitated comparison, linking, and reviewing of models (e.g. Berger et al. 2008) and the re-use of useful and validated submodels of particular behaviours (“pattern-oriented theory development”; Railsback & Grimm 2019).

6.2
We have summarized issues and challenges that could prevent wider and more coherent use of ODD and have presented possible solutions. We also provided an outlook on possible future developments. Overall, by promoting and improving ODD we hope to contribute to the maturation of agent-based modelling as a scientific tool (Lorscheid et al. 2019). The language of mathematics developed over hundreds of years, so we cannot expect a lingua franca for ABMs, or simulation models in general, to emerge within a few years.

6.3
A major, and perhaps most important, part of this article is the supplements, which contain guidance, templates, and examples. We therefore summarized these supplements in Table 1. We encourage developers and users of ABMs to use this material and thereby contribute to the development of ODD and related standards. Feedback and new ideas are welcome as well, for example via the forum on CoMSES.net. We also ask users of ODD to please continue to cite the ODD publications (Grimm et al. 2006 and this article) so that the use of ODD can be monitored.

Acknowledgements
We thank Ellen-Wien Augustijn and Friedrich Bohn for helpful comments on this article, Ian Dennis Miller for the hint to “Literate Programming”, and numerous ODD users for their feedback. JGe and JGP acknowledge funding from the Scottish Government Rural Affairs, Food and Environment Strategic Research Programme 2016–2021, Work Packages 2.4: “Rural Industries” and 3.3: “Food Security”. DLD was supported by the Greater Everglades Priority Ecosystem Science program. Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government. VG, AM and M-SR acknowledge funding from the Deutsche Forschungsgemeinschaft in the framework of the BioMove Research Training Group (DFG-GRK 2118/1).
Notes
https://agilemanifesto.org/.
Literate programming. (n.d.) In Wikipedia. Retrieved October 29, 2019, from https://en.wikipedia.org/wiki/Literate_programming.

--- END CONTEXT FILE: data/abm_odd_evaluator/context_docs/odd.md ---
--- START CONTEXT FILE: data/abm_odd_evaluator/context_docs/evaluation criteria.md ---
Given the following documentation and code for an agent-based model (please provide the documentation and code here), please perform the following analysis:

Describe the overall quality of the model based on the provided documentation and code.
Consider aspects such as clarity of the model's purpose, the level of detail in the design and implementation, the transparency of the agent rules and interactions, and the quality of the documentation.

Evaluate whether this model could be considered a "high quality" agent-based model. Justify your assessment by referring to specific criteria discussed in the handbook. This should include, but not be limited to:

The clarity and justification of the model's goals. Is it clear what the model aims to achieve (e.g., theoretical exposition, empirical exploration, prediction, illustration)?

The explicitness and grounding of the ontological structure. Are the agents, their attributes, and their relationships clearly defined and justified?

The connection to evidence, experiences, or data. Is it clear how the model relates to the real-world phenomenon it intends to represent? Is this relationship well-documented?

The handling and documentation of modeling assumptions. Are the assumptions clearly stated and, where possible, justified?

The efforts towards verification. Is there evidence that the model behaves as intended by the programmer?

The consideration of validation. Are there attempts to assess the model's credibility against external references (data, other models, expert knowledge)?

The quality and completeness of the documentation, ideally following a structured approach like the ODD protocol. Does the documentation enable understanding, replication, and further development?

The transparency and readability of the code. Is the code well-structured, commented, and easy to understand?

Suggest specific improvements that could enhance the quality of this agent-based model. These suggestions should be actionable and grounded in the principles discussed in the handbook. Consider areas such as:

Documentation: Could the documentation be more comprehensive (e.g., by using the ODD protocol)? Are the assumptions and design decisions sufficiently explained?

Model Design: Is the ontological structure well-defined and justified? Are the agent behaviors clearly specified and motivated?

Verification and Validation: Are there opportunities for more rigorous verification (e.g., through systematic testing)? What steps could be taken to validate the model against relevant data or other models? Could stakeholder involvement enhance validation?

Code Quality: Are there areas in the code that could be made more readable, modular, or efficient?

Consideration of Purpose: Is the model being used for its intended purpose? Are the limitations of the model in relation to its purpose clearly acknowledged?
--- END CONTEXT FILE: data/abm_odd_evaluator/context_docs/evaluation criteria.md ---


## Input Specification
The end-user will provide input matching the following description:
model code and documentation

The user's input will be provided below, marked by the `{{INPUT}}` placeholder.

Instructions for the User's Input:
by using a tool like diringest or gitingest to create a digest of the whole model's code into a single markdown file

**User Input:**
```
{{INPUT}}
```

## Output Specification
You must generate an output that adheres *exactly* to the following specifications:

**Output Description:**
High quality evaluation report based on criteria and structure from the CONTEXT

**Formatting and Structure Requirements:**
in markdown format

## Constraints & Guidelines
Adhere strictly to the following constraints and guidelines:
*   **Tone:** Maintain a Factual tone.
*   Focus solely on the provided input and context (if any) to generate the response. Do not add information not present in the source materials unless explicitly asked to.
*   Be precise and follow all formatting instructions meticulously.

## Examples (Optional)


Now, generate the complete TASK_PERFORMING_PROMPT based on the structure and content defined above.