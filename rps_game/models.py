from django.db import models

class Room(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=100)
  player1 = models.CharField(max_length=20, blank=True, null=True)
  player2 = models.CharField(max_length=20, blank=True, null=True)
  player1_move = models.CharField(max_length=20, blank=True, null=True)
  player2_move = models.CharField(max_length=20, blank=True, null=True)
  player1_wins = models.IntegerField(default=0)
  player2_wins = models.IntegerField(default=0)
  final_result = models.CharField(max_length=10, blank=True, null=True)
  round_result = models.CharField(max_length=10, blank=True, null=True)
  all_moves = models.TextField(default='[]')

  def add_move(self, player_name, move):
    import json
    moves = json.loads(self.all_moves)
    moves.append({'player': player_name, 'move': move})
    self.all_moves = json.dumps(moves)
    self.save()

  def get_all_moves(self):
    import json
    return json.loads(self.all_moves)

  def __str__(self):
    return self.name

