# Pokémon: Meridian — Chapter 1, Scene 4: Awakening
**Status: OWNER APPROVED** (2026-11-10, including revised dialogue and required journal interaction)  
**Creative owner:** ChatGPT Project  
**Implementation owner:** Codex  
**Environment/visual owner:** ChatGPT Work (preserve approved Medical Facility and Landing Camp design)  
**Scope:** Scene 4 only. Scene 5 and remaining Chapter 1 are **not approved**.

## Narrative intent
The player awakens three days after the storm, discovers that their humble researcher father did not survive, and meets the wealthy, politically influential father of their rival. The rival's father is sincerely compassionate; the trusted mentor/parental relationship develops **gradually**, not instantly. The player's father's legacy is a recurring theme. No gratuitous visual depiction of his death.

## Scene 4A — A Different Kind of Morning
**Location:** Fully operational Expedition Medical Facility, Aevor.  
**Presentation:** Black screen; crashing waves fade into silence; distant voices; soft medical sounds. Morning sunlight through a window reveals a functional facility. The player lies in a medical bed, having sustained a significant head injury. Settlement life is audible outside.

**UNKNOWN VOICE:** “Their pulse is steady.”  
**SECOND VOICE:** “And the swelling?”  
**UNKNOWN VOICE:** “Going down. That's encouraging.”  
**SECOND VOICE:** “How long?”  
**UNKNOWN VOICE:** “Nearly three days.”

Fade in. Nurse notices movement.

**NURSE:** “Doctor! They're awake!”  
**DOCTOR:** “Easy. Don't try to get up just yet.”  
“You've been unconscious for almost three days.”  
“Do you remember what happened?”

**Player response choice:**
- **“There was a storm...”** → **DOCTOR:** “That's right. The ship took considerable damage during our approach.”
- **“Where's my father?”** → **DOCTOR:** “...Let's make sure you're all right first.”
- **“Where am I?”** → **DOCTOR:** “You're in Meridian. The expedition's medical headquarters.”

All branches converge.

**DOCTOR:** “Our rescue crews brought you here after the ship reached shore. You had a significant head injury, but you've been recovering well.”  
“Your father was listed as part of the research personnel, correct?”

Player nods. Doctor looks toward door.

**DOCTOR:** “There's someone who would like to speak with you.”  
“I'll give you a moment.”

Doctor and nurse leave. Player notices permanent buildings, people and a blue-and-gold expedition flag outside.

## Scene 4B — The Man Who Stayed
The rival's father enters, well dressed and exhausted, with a small leather-bound notebook. He is **not named yet**; this document uses role labels until the owner approves a name.

**RIVAL'S FATHER:** “You're awake.”  
“That's good. Very good.”  
“I've been checking on you these last few days.”  
“I don't believe we've been properly introduced.”  
“I'm responsible for much of the expedition's work with the people of Aevor. Your father and I corresponded before the voyage.”  
“He spoke highly of you.”

**PLAYER:** “Where is he?”  
**RIVAL'S FATHER:** “...I was hoping we'd have this conversation under better circumstances.”  
**PLAYER:** “Is he here?”  
**RIVAL'S FATHER:** “No.”  
**RIVAL'S FATHER:** **“Your father didn't make it through the storm.”**

**Presentation:** Music stops; camera holds; allow a substantial pause.

**RIVAL'S FATHER:** “The ship was struck hard during the crossing. Several compartments were damaged.”  
“He was helping other passengers reach safety when the lower passageway flooded.”  
“I'm sorry.”

**Player response choice:**
- **Remain silent** → **RIVAL'S FATHER:** “You don't have to say anything.”
- **“No. He was right there...”** → **RIVAL'S FATHER:** “I know. You went to sleep expecting to see him again.”
- **“Why didn't anyone save him?”** → **RIVAL'S FATHER:** “You have every right to be angry. I wish I had an answer that would make this easier.”

All branches converge; do not treat one reaction as canon over the others.

He sets the journal on the bedside table.

**RIVAL'S FATHER:** “He asked me to look over some of his research when he arrived.”  
“I'd been looking forward to meeting him in person.”  
“He wasn't a wealthy man. He didn't have powerful friends in the government.”  
“But he understood things about our world that people in my position never bothered to learn.”  
“Your father's work mattered.”  
“And I intend to make sure it wasn't for nothing.”

He stands, sincerely supportive but not declaring himself the player's replacement father.

**RIVAL'S FATHER:** “You have a place here. Whatever you need, we'll see that you have it.”  
“But today, you should rest.”  
“When you're ready, come find me at headquarters.”  
**“I'd like to show you the place your father helped us build.”**

He exits.

## Scene 4C — What He Left Behind (mandatory item interaction)
Player gains control in the medical room. The leather-bound notebook is on the bedside table, visible and interactable.

**Object:** Father's Research Journal  
*The cover is worn. Several pages have been repaired with tape.*  
*Inside are observations about declining ecosystems, Pokémon migration patterns, and the possibility of restoring damaged habitats.*  
*A handwritten note is tucked between the pages.*

Journal opening note:

> Knowledge means very little if we aren't willing to use it to help someone.
>
> Whatever happens, keep asking questions.
>
> There's always something worth understanding.

**Obtain Key Item:** **Father's Research Journal**. Keep it permanently in Key Items; later lore/journal sections can be added in separately approved episodes.

### Mandatory soft-lock prevention / exit gate
- **Before journal collected:** attempting to leave the opening medical room displays exactly the approved cue **“Wait... Dad's journal is still on the table.”** and turns or directs the player toward the bedside table. Do not allow progression out until journal is obtained.
- Journal pickup sets a **persistent, save-safe one-time story flag**, adds the Key Item exactly once, and updates the current objective to **Visit Expedition Headquarters**.
- **After journal collected:** exit works normally; repeated object interaction does not duplicate items or replay the one-time reward.
- On save/reload, journal inventory/flag and exit behavior remain consistent. Avoid using a temporary variable that resets and blocks progression.
- If script interruption/failure happens during pickup, the implementation must recover without trapping the player.
- Codex should use the repository's actual scripting conventions/flag definitions; **names below are examples only**, not mandated identifiers.

## Scene 5 transition (boundary only; separate approval)
After exiting, player enters the already established headquarters settlement. Nearby medical staff may acknowledge that the father was respected and contributed to the expedition. Objective: **Visit Expedition Headquarters**. Full Scene 5 staging, tour and dialogue are **not yet approved**.

## Implementation/QA handoff
Codex should implement from this approved scene once the actual playable medical-room map and reliable story flow are available; coordinate map resources and NPC placements with Work. Verify in ROM/emulator:
1. Scene triggers only at intended point following the storm and preserves continuation after save/load.
2. All three doctor and grief dialogue branches converge correctly.
3. The exact two owner-revised lines are present.
4. Before pickup, attempted exit gives reminder and cannot bypass pickup.
5. Journal is a Key Item, obtained once; repeated interactions and save/reload do not duplicate.
6. After pickup, door exits normally and HQ objective is set.
7. No crash or stranded state on repeated interaction or reentry.

No emulator test is claimed by this document. Work preserves approved visual facility; do not substitute concept images or temporary generic artwork for final visual approval.
