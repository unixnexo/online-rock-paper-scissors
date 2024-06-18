import random
import string
import time
import json
from django.http import JsonResponse
from .models import Room
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_room(request):
  context = {}
  if request.method == 'POST':
    if request.POST.get('action') == 'create_room':
      room_name = generate_random_string(10)
      player1_name = generate_random_string(5)
      room = Room.objects.create(name=room_name, player1=player1_name)
      
      # Store player1_name in session
      request.session['player_name'] = player1_name
      request.session['player_role'] = 'player1'
      
      return redirect('room', room_name=room.name)

    elif request.POST.get('action') == 'join_room':
      room_name = request.POST.get('room_name')
      try:
        room = Room.objects.get(name=room_name)
        if room.player2:
          context['error'] = 'Room is already full.'
        else:
          player2_name = generate_random_string(5)
          room.player2 = player2_name
          room.save()
          
          # Store player2_name in session
          request.session['player_name'] = player2_name
          request.session['player_role'] = 'player2'
          
          return redirect('game', room_name=room.name)
      except Room.DoesNotExist:
        context['error'] = 'Room does not exist.'
  
  return render(request, 'create_room.html', context)


def game(request, room_name):
  player_name = request.session.get('player_name', 'Unknown')
  player_role = request.session.get('player_role', 'Unknown')
  
  context = {
    'room_name': room_name,
    'player_name': player_name,
    'player_role': player_role,
  }

  return render(request, 'game.html', context)


def room(request, room_name):
  try:
    room = Room.objects.get(name=room_name)
    context = {
      'room_name': room.name,
      'player1': room.player1,
      'player2': room.player2
    }
    return render(request, 'room.html', context)
  except Room.DoesNotExist:
    return redirect('create_room')
    

def check_room_status(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
        if room.player2:
            return JsonResponse({'status': 'full', 'player2': room.player2})
        else:
            return JsonResponse({'status': 'empty'})
    except Room.DoesNotExist:
        return JsonResponse({'status': 'not_found'})


@csrf_exempt
def save_move(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      move = data.get('move')
      room_name = data.get('room_name')

      room = Room.objects.get(name=room_name)

      player_name = request.session.get('player_name')
      if player_name == room.player1:
        room.player1_move = move
      elif player_name == room.player2:
        room.player2_move = move
      else:
        return JsonResponse({'error': 'Unauthorized or invalid move request'}, status=403)

      # method is from model
      room.add_move(player_name, move)
      room.save()

      if room.player1_move is not None and room.player2_move is not None:
        result = determine_winner(room.player1_move, room.player2_move)
        timestamp = int(time.time())
        room.round_result = f"{result}_{timestamp}"

        if result == 'player1':
          room.player1_wins += 1
        elif result == 'player2':
          room.player2_wins += 1

        room.player1_move = None
        room.player2_move = None

        if room.player1_wins == 3:
          room.final_result = 'player1'
        elif room.player2_wins == 3:
          room.final_result = 'player2'

        room.save()

      return JsonResponse({'message': 'Move saved successfully'})

    except Room.DoesNotExist:
      return JsonResponse({'error': 'Room not found'}, status=404)

  return JsonResponse({'error': 'Invalid request'}, status=400)
  

def get_result(request, room_name):
  try:
    room = Room.objects.get(name=room_name)

    # method is from model
    all_moves = room.get_all_moves()

    # Get the last move if there are any moves
    last_move = all_moves[-2:] if len(all_moves) >= 2 else all_moves

    return JsonResponse({
      'result': room.final_result,
      'player1_wins': room.player1_wins,
      'player2_wins': room.player2_wins,
      'round_result': room.round_result,
      'all_moves': all_moves,
      'last_move': last_move, 
    })

  except Room.DoesNotExist:
    return JsonResponse({'error': 'Room not found'}, status=404)


def determine_winner(move1, move2):
  if move1 == move2:
    return 'draw'
  elif (move1 == 'rock' and move2 == 'scissors') or \
       (move1 == 'paper' and move2 == 'rock') or \
       (move1 == 'scissors' and move2 == 'paper'):
    return 'player1'
  else:
    return 'player2'





###### test