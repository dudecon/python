import bpy

Episode_Number = 371

labels_Text = """00:00 Shamus making content on the DL
01:56 Unity whitepapers
13:18 Endless Space 2 on Linux
17:24 Darksiders 2: Deathinitive Edition
18:42 The Tale of the Invalid Verification Codes
37:06 Wireless Headphones and the wrong way to do battery mounting.
42:53 Patreon Census
49:12 Mailbag: Favourite RPG Choices
56:49 Mailbag: Games you have slept on
1:02:45 Outro"""

curscene = bpy.data.scenes[0]
curscene.render.filepath = f"//Diecast {Episode_Number}"
cursequences = curscene.sequence_editor.sequences
# update the audio
cursequences[0].name = f'diecast{Episode_Number}.ogg'
cursequences[0].sound.filepath = f'//diecast{Episode_Number}.ogg'
cursequences[2].text = f'{Episode_Number}'
cursequences[4].text = f'{Episode_Number}'
curscene.render.filepath = f"//Diecast {Episode_Number}"

FPS = curscene.render.fps

def find_frame(timestamp_label):
    total_secs = 0
    digits = timestamp_label.split(':')
    i = 0
    while len(digits) > 0:
        total_secs += (60**i)*int(digits.pop())
        i += 1
    frame = FPS * total_secs
    return frame

frame_labels = []
for label in labels_Text.split('\n'):
    splitlabel = label.split()
    if len(splitlabel) < 2: continue
    tstamp = splitlabel[0]
    labeltxt = ' '.join(splitlabel[1:])
    frmstrt = find_frame(tstamp)
    frame_labels.append([frmstrt,labeltxt])
frame_labels[0][0] = find_frame('10')
frame_labels.append((frame_labels[-1][0] + find_frame('109'),"END"))

FONT = bpy.data.fonts[0]
for i in range(len(frame_labels)-1):
    strt = frame_labels[i][0]
    endt = frame_labels[i+1][0]-find_frame('10')
    colr = cursequences.new_effect('bkgd box', 'COLOR', 6, strt, frame_end=endt)
    colr.color = (0,0,0)
    colr.transform.scale_x = 0.95
    colr.transform.scale_y = 0.618
    colr.blend_type = 'ALPHA_OVER'
    colr.blend_alpha = 0.8
    strp = cursequences.new_effect('topic', 'TEXT', 7, strt, frame_end=endt)
    strp.text = frame_labels[i][1]
    strp.font = FONT
    strp.font_size = 131
    strp.wrap_width = 0.85
    

#cursequences.new_effect(name, type, channel, frame_start)
