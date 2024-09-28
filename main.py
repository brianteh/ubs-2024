import json
import re
import os
from flask import Flask, jsonify, request
from collections import defaultdict, deque
app = Flask(__name__)
app.debug = True
class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]
#app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/') to fix nginx proxy pass problems
#GET example
@app.route('/hello', methods=['GET'])
def get_example():
   return jsonify(["GET good"])


#POST EXAMPLE
@app.route('/pello', methods=['POST'])
def post_example():
   return jsonify(["POST good"])


#Solve the Wordle
@app.route('/wordle-game', methods=['POST'])
def solve_wordle():
   default_ans={"guess":"slate"}
   data = json.loads(request.data)
   if(len(data["guessHistory"])==0):
      return jsonify(default_ans)
   

   return request.data

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def solve_kazuma():
   return {}

# ctf
@app.route('/payload_crackme', methods=['GET'])
def solve_ctf_crack_me():
   return "111-1111111" 
@app.route('/payload_stack', methods=['GET'])
def solve_ctf_stack():
   return 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xfa\x11\x40\x00\n'

#bug fixer
@app.route('/bugfixer/p1', methods=['POST'])
def solve_bug_fixer():
   # Get the input JSON
   json_string = request.data.decode('utf-8') 
   json_string = json_string.replace('(', '[').replace(')', ']')
   data=json.loads(json_string)
   ans_arr=[]
   for k in range(len(data)):
   
      times = data[k]['time']
      prerequisites = data[k]['prerequisites']

      n = len(times)  # Number of projects

      # Step 1: Build the graph and initialize data structures
      graph = defaultdict(list)
      in_degree = [0] * n
      min_hours = [0] * n

      # Create the graph and in-degree count
      for a, b in prerequisites:
         graph[a-1].append(b-1)  # Convert to 0-based index
         in_degree[b-1] += 1

      # Step 2: Initialize the min_hours with the project times
      for i in range(n):
         min_hours[i] = times[i]

      # Step 3: Topological sort using Kahn's Algorithm
      queue = deque()
      
      # Start with projects that have no prerequisites
      for i in range(n):
         if in_degree[i] == 0:
            queue.append(i)

      while queue:
         current = queue.popleft()

         for neighbor in graph[current]:
            # Update the minimum hours for the neighbor
            min_hours[neighbor] = max(min_hours[neighbor], min_hours[current] + times[neighbor])
            in_degree[neighbor] -= 1
            
            if in_degree[neighbor] == 0:
                  queue.append(neighbor)

      # The answer is the maximum of the min_hours
      result = max(min_hours)
      ans_arr.append(result)
   return jsonify(ans_arr)

def max_bugsfixed(bug_infos):
   arr=[]
   for i in range(len(bug_infos)):
      bug_seq = bug_infos[i]['bugseq']
      
      # Sort bugs by their limit
      bug_seq.sort(key=lambda x: x[1])  # Sort by limit
      
      total_time = 0
      completed_bugs = 0
      
      for difficulty, limit in bug_seq:
         total_time += difficulty
         if total_time <= limit:
               completed_bugs += 1
         else:
               break  # No need to check further as they are sorted by limit

      arr.append(completed_bugs)
   return arr

@app.route('/bugfixer/p2', methods=['POST'])
def bugfixer():
   data = json.loads(request.data)
   result = max_bugsfixed(data)
   return jsonify(result)
# decode and conquer
@app.route('/ub5-flags', methods=['GET'])
def solve_decode():
   data={
   "sanityScroll": {
      "flag": os.environ.get('FLAG')
   },
   "openAiExploration": {
      "flag": "FLAG_CONTENT_HERE"
   },
   "dictionaryAttack": {
      "flag": "UB5{FLAG_CONTENT_HERE}",
      "password": "PASSWORD_HERE"
   },
   "pictureSteganography": {
      "flagOne": "UB5-1{FLAG_ONE_CONTENTS_HERE}",
      "flagTwo": "UB5-2{FLAG_TWO_CONTENTS_HERE}"
   },
   "reverseEngineeringTheDeal": {
      "flag": "FLAG_CONTENT_HERE",
      "key": "KEY_HERE"
   }
      }
   return jsonify(data)


# Klotski
def generate_2d(board_string):
   arr = []
   i=0
   while i<len(board_string):
      arr.append(list(board_string[i:i+4]))
      i+=4
   return arr

def moving(moves_string):

   global g_arr
   moves_string = list(moves_string)
   
   for i in range(0,len(moves_string),2):
      move(get_position_arr(g_arr,moves_string[i]),moves_string[i+1])


def get_position_arr(arr_2d,target):

    arr=[]
    for i in range(len(arr_2d)):
        for j in range(len(arr_2d[i])):
            if(target == arr_2d[i][j]):
                pos = [i,j]
                arr.append(pos)
    return arr

def move(pos_arr,dir):
   global g_arr
   visited_pos =[False]*len(pos_arr)
   temp_pos_arr = pos_arr
   

   while (False in visited_pos):
      for j in range(len(visited_pos)):
         if(visited_pos[j]==True):
               continue
         if not(temp_pos_arr[j][1] == len(g_arr[j])-1):
               if(g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]+1]=="@" and dir=="E"):
                  temp = g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]]
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]] = "@"
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]+1]=temp
               
                  visited_pos[j]=True
                  continue
         if not(temp_pos_arr[j][0]==0):
               if(g_arr[temp_pos_arr[j][0]-1][temp_pos_arr[j][1]]=="@" and dir=="N"):
                  temp = g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]]
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]] = "@"
                  g_arr[temp_pos_arr[j][0]-1][temp_pos_arr[j][1]]=temp
                  
                  visited_pos[j]=True
                  continue
         if not(temp_pos_arr[j][1] == 0 ):
               if(g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]-1]=="@" and dir=="W"):
                  temp = g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]]
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]] = "@"
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]-1]=temp
                  
                  visited_pos[j]=True
                  continue
         if not(temp_pos_arr[j][0] == len(g_arr)-1):
               if(g_arr[temp_pos_arr[j][0]+1][temp_pos_arr[j][1]]=="@" and dir=="S"):
                  temp = g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]]
                  g_arr[temp_pos_arr[j][0]][temp_pos_arr[j][1]] = "@"
                  g_arr[temp_pos_arr[j][0]+1][temp_pos_arr[j][1]]=temp
               
                  visited_pos[j]=True
                  continue





g_arr=None

@app.route('/klotski', methods=['POST'])
def klotski():
   global g_arr
   data = json.loads(request.data)
   print(data)
   ans=[]
   for d in range(len(data)):
      g_arr = generate_2d(data[d]["board"])
      moving(data[d]["moves"])
      ans_string=""
      for h in range(len(g_arr)):
         for k in range(len(g_arr[h])):
               ans_string+=g_arr[h][k]
      ans.append(ans_string)

   return jsonify(ans)

#Clumsy Programmer
# Function to check if two words differ by exactly one character
def is_one_letter_different(word1, word2):
   if len(word1) != len(word2):
      return False
   difference_count = 0
   for i in range(len(word1)):
      if word1[i] != word2[i]:
         difference_count += 1
      if difference_count > 1:
         return False
   return difference_count == 1

# Function to correct mistyped words using the provided dictionary
def correct_mistypes(data):
   corrections = []
   for entry in data:
      dictionary = entry["dictionary"]
      mistypes = entry["mistypes"]
      corrected_words = []
      
      # Iterate over each mistyped word
      for mistyped_word in mistypes:
         # Find the correct word in the dictionary
         for correct_word in dictionary:
               if is_one_letter_different(mistyped_word, correct_word):
                  corrected_words.append(correct_word)
                  break
      
      corrections.append({"corrections": corrected_words})
   
   return corrections
@app.route('/the-clumsy-programmer',methods=['POST'])
def solve_clumsy():
   json_string = request.data.decode('utf-8')
   corrected_json_string = re.sub(r',(\s*[\]}])', r'\1', json_string) 
   data = json.loads(corrected_json_string)
   corrected_data = correct_mistypes(data)  
   # Get corrections for mistyped words
   return jsonify(corrected_data)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000)