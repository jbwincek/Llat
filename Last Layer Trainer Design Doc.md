#Last Layer Trainer Design Doc / roadmap 

###algorithm_grabber.py:
grabs algorithms off of algdb.net and saves them as a json file.

###trainer.py
  * layout:
    * title bar at the top
    * action area in the middle
    * response/satus bar at the bottom
  * features:
    * voice recognition
    * training queue
    * algorithm preference display
      * (load/save from disk)
      * (load alg repositories from disk)
  * voice commands:
    * list_perms
    * next_slide
    * previous_slide
    * quit
    * thank_you
    * train_more
    * select_choice
    
    
###Roadmap and progress
- [ ] user interface
  - [ ] npyscreen.NPSAppManaged main app class
    - [ ] addForm splash screen while initializing
    - [ ] addForm menu screen
    - [ ] addForm training mode
  - [ ] splash screen
    - [ ] draw figlets style title
    - [ ] algorithms loading
    - [ ] preferences loading
    - [ ] silence for Microphone initialization 
  - [ ] menu system 
    - [ ] start training
    - [ ] help 
    