## Pre install pygame
Follow here to install pygame:

https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation


## leben
```
python3 leben/main.py --seele human
python3 leben/main.py --seele random
python3 leben/main.py --seele rulebase
python3 leben/main.py --seele reinforcement
```

Life simulator

### training leben model
```
python leben/main.py --mode train --seele reinforcement
```

## dog fight

```
python3 dog_fight/main.py
```

2 person dog fighting game with sound record.

Sound effect from Home World: Desert of Kharak.

Sound effect extracted by Lev_Astov from reddit.

### Control:

| Player | Direction  | Gatlin  | Missle |
| ------ | ---------- | ------- | ------ |
| 0      | A/D        | L_Shift | L_Ctrl |
| 1      | Left/Right | R_Shift | R_Ctrl |

----
### Dev log:
Jan 26:
* Tried Reinforcement learning on simplified task:
  * No death penalty.
  * Only keeps two actions: Forward and Turn Left. (Otherwise, the system can easily stuck into deadloop like keeps going back and forth, or keep turning left and right, making it hard to train).
  * While training, actions are sampled from softmax output.
  * While inference, actions are picked by argmax from output.
  * The result looks good, while model see an object in front it will go forward, otherwise it will turn left.
* Open problems:
  * How to train with four actions? The model need to somehow remember that it is turning left last time so it can keep turning left, so it won't stuck into infinite loop.
  * TODO: Try to add some kind of residual.
  * Is it possible to let the model perform two action at the same time?
