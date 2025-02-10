s = """	 tryop.com	 /public_html	
Not Redirected
3d.tryop.com	 /public_html/3d	 http://peripheralarbor.com/commission/index.html	
 Off	 
	 ai.tryop.com	 /public_html/ai	 https://docs.google.com/document/d/1mL1v3oZHmu-ecSKtl5tP9hkAEn5WBMGBGFbH3Garf_w	
 Off	 
	 author.tryop.com	 /public_html/author	 http://peripheralarbor.com/author.htm	
 Off	 
	 bible.tryop.com	 /public_html/bible	 http://peripheralarbor.com/Bible/	
 Off	 
	 f.tryop.com	 /public_html/f.tryop.com	 http://www.peripheralarbor.com/fledgeling/	
 Off	 
	 handyman.tryop.com	 /public_html/Handyman	 http://tryop.com/Handyman/	
 Off	 
	 ip.tryop.com	 /public_html/ip	
Not Redirected
 Off	 
	 junk.tryop.com	 /public_html/junk.tryop.com	
Not Redirected
 Off	 
	 laser.tryop.com	 /public_html	 http://peripheralarbor.com/gallery/v/Projects/Woodworking/Lasers/	
 Off	 
	 mc.tryop.com	 /public_html/mc	 http://peripheralarbor.com/minecraft/minecraftscripts.html	
 Off	 
	 paul.tryop.com	 /public_html/paul.tryop.com	 https://peripheralarbor.com/Resume_Spooner.pdf	
 Off	 
	 piano.tryop.com	 /public_html/piano	 https://www.tryop.com/piano/	
 Off
	 sub.tryop.com	 /public_html/sub	 http://peripheralarbor.com/subscribe.htm	
 Off	 
	 tetpln.tryop.com	 /public_html/tetpln.tryop.com	 https://peripheralarbor.com/gallery/CG+Art/TetPln/	
 Off	 

 uv.tryop.com	 /public_html	
Not Redirected"""

"""<img src="3d.tryop.com.png" title="QR code for this page">"""
# https://barcode.tec-it.com/en/MobileQRCode
# set download type to PNG
# set quiet zone to 4 pixels
# re-encode as indexed 2 color in the GIMP
# save with image resolution only

print('<table border="0" cellpadding="5" cellspacing="7"><tbody>')

opposite = False
for i in s.split('\n'):
    e = i.strip('\t').split('\t')
    if len(e) == 2:
        url = e[0].strip()
        second = e[1].strip()
        if len(second) == 0: continue
    elif len(e) == 3:
        url = e[0].strip()
        second = e[2].strip()
    else: continue
    link = "http://"+url
    image = url+".png"
    if opposite:
        print(f'<tr id = "{url}"><td><a href="{link}"><img src="{image}" title="QR code for this page"></a></td><td><a href="{link}">{link}</a></td><td>description</td></tr>\n\n')
        opposite = False
    else:
        print(f'<tr id = "{url}"><td>description</td><td><a href="{link}">{link}</a></td><td><a href="{link}"><img src="{image}" title="QR code for this page"></a></td></tr>\n\n')
        opposite = True

print("</tbody></table>")
