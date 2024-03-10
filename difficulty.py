class Difficulty():
    def __init__(self, my_dict, level):
        self.my_dict = my_dict
        self.level = level
        self.subset_dict = self.my_dict[self.level]

    def update_difficulty(self,  new_level):
        self.level = new_level
        self.subset_dict = self.my_dict[self.level]

difficulty_dict = {
  "easy" : {
  "enemy_speed" : 5,
  "enemy_spawn_time" : 400,
  "enemy_spawn_location" : 0,
  "target_color_duration" : 15000,
  "score_increase" : 1,
  "score_decrease" : 1
  },
  "medium" : {
  "enemy_speed" : 8,
  "enemy_spawn_time" : 400,
  "enemy_spawn_location" : 100,
  "target_color_duration" : 10000,
  "score_increase" : 1,
  "score_decrease" : 1
  },
  "hard" : {
  "enemy_speed" : 11,
  "enemy_spawn_time" : 200,
  "enemy_spawn_location" : 200,
  "target_color_duration" : 8000,
  "score_increase" : 2,
  "score_decrease" : 1
  },
  "nightmare" : {
  "enemy_speed" : 15,
  "enemy_spawn_time" : 100,
  "enemy_spawn_location" : 500,
  "target_color_duration" : 5000,
  "score_increase" : 3,
  "score_decrease" : 2
  }
}