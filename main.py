from dotenv import load_dotenv
import os
import openai

load_dotenv()


openai.api_key = os.environ.get('OPENAI_KEY')

model = "gpt-3.5-turbo"

# prompt = '''
# Generate a YouTube Video title from the Chem 1A General Chemistry Lecture in the format "Chem 1A: <title>. Lecture 1, Part 2 (Starts at <time>)"

# 00:00 - Microscopic view reveals silicon wafer's surface roughness and atomic structure.
# Chemistry studies molecular scale, demonstrated via observable reactions and explosions.
# The instructor quizzes students on understanding length scales in chemistry.
# '''

prompt = '''
137
00:10:02,920 --> 00:10:09,720
 OK, and so what I want to do now is give you another quiz.

138
00:10:09,720 --> 00:10:12,440
 And that is you don't have to answer yet.

139
00:10:12,440 --> 00:10:17,440
 Since the length scales are so central in understanding chemistry and since I defined chemistry through

140
00:10:17,440 --> 00:10:23,000
 the length scales, from very small length scales to very large length scales, up to

141
00:10:23,000 --> 00:10:28,560
 a micron, I want to make sure that you guys understand what length scales are.

142
00:10:28,560 --> 00:10:33,520
 And so the question, the quiz that I have posed is how many angstroms are there in a

143
00:10:33,520 --> 00:10:34,520
 meter?

144
00:10:34,520 --> 00:10:41,520
 And I gave you a table and I only said it once how many angstroms are there in a nanometer

145
00:10:41,520 --> 00:10:43,040
 before.

146
00:10:43,040 --> 00:10:48,080
 But if you don't know, what we would do is then try it again.

147
00:10:48,080 --> 00:10:51,000
 And the question is how many angstroms are there in a meter?

148
00:10:51,000 --> 00:10:55,800
 And I gave you the table saying that a meter has 100 centimeters.

149
00:10:55,800 --> 00:10:58,160
 It has a thousand millimeters.

150
00:10:58,160 --> 00:11:03,480
 It has a million micrometers and a billion nanometers.

151
00:11:03,480 --> 00:11:05,880
 So go ahead, you can start answering.

152
00:11:05,880 --> 00:11:09,880
 But don't talk to your neighbors yet.

153
00:11:09,880 --> 00:11:21,800
 Of course, if you got the wrong answer, you would still get the credit for participating.

154
00:11:21,800 --> 00:11:41,280
 You better get the right answer.

155
00:11:41,280 --> 00:11:48,840
 You guys are pretty fast.

156
00:11:48,840 --> 00:11:53,400
 Those that do not have clickers either get the clickers because that's how you're going

157
00:11:53,400 --> 00:11:56,400
 to get credit for participating.

158
00:11:56,400 --> 00:11:59,880
 And if it doesn't work, then you'd have to register it.

159
00:11:59,880 --> 00:12:04,480
 And if that doesn't work, you'd have to talk to her email to Pratima who is left.

160
00:12:04,480 --> 00:12:07,760
 But she still reads her emails.

161
00:12:07,760 --> 00:12:13,160
 All right, let's see what the distribution of results are.

162
00:12:13,160 --> 00:12:16,560
 And it's pretty broad.

163
00:12:16,560 --> 00:12:20,440
 Most of you think it's A, but there is a wide distribution.

164
00:12:20,440 --> 00:12:24,280
 Of course, all of the above cannot be the right answer because none of the above is not

165
00:12:24,280 --> 00:12:27,920
 the answer and both cannot be.

166
00:12:27,920 --> 00:12:32,520
 Now let's do this again and this time you guys can talk to each other.

167
00:12:32,520 --> 00:12:34,880
 So let's try again, talk to each other.

168
00:12:34,880 --> 00:12:50,160
 Once we converge, let's see how this works.

169
00:12:50,160 --> 00:13:15,920
 All right, let's go.

170
00:13:15,920 --> 00:13:43,920
 Okay, I'm going to give you 20 more seconds.

171
00:13:43,920 --> 00:14:10,920
 And then I'm going to show you the results as well.

172
00:14:10,920 --> 00:14:15,720
 Yeah, you can change your answer.

173
00:14:15,720 --> 00:14:21,320
 It's pretty fun to play with it.

174
00:14:21,320 --> 00:14:22,720
 All right, so.

175
00:14:22,720 --> 00:14:26,040
 So yeah, I guess you either know the answer or you're don't.

176
00:14:26,040 --> 00:14:29,480
 And the hope is that when you talk to your neighbors, that's the way you learn, which

177
00:14:29,480 --> 00:14:34,520
 is true in this case because we, the right answer is indeed 10 billion.

178
00:14:34,520 --> 00:14:44,480
 So this means that if I take a meter, a meter, I can put 10 billion molecules, hydrogen molecules,

179
00:14:44,480 --> 00:14:50,240
 which have about a bond length of an angstrom, a little bit less, can put 10 million of them

180
00:14:50,240 --> 00:14:58,800
 in a line inside a meter, which is quite amazing because 10 billion is not something we can

181
00:14:58,800 --> 00:15:00,880
 understand easily.

Summarize in up to 10 words. Include the start timestamp.
'''

def get_messages(prompt):
  return [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]


response = openai.ChatCompletion.create(
  model=model,
  messages=get_messages(prompt)
)

print(response['choices'][0]['message']['content'])
