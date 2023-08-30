import code_src.p1 as q1
import code_src.p2 as q2
import code_src.p3 as q3
import code_src.p4 as q4

def q_1_driver():
    path = 'images\coins.png'
    
    hist = q1.get_histogram(path)

def q_2_driver():
    path = 'images\coins.png'
    
    bin_img = q2.otsu(path)

def q_3_driver():
    text_image_path = 'Images/IIScText.png'
    depth_image_path = 'Images/IIScTextDepth.png'
    background_image_path = 'Images/IIScMainBuilding.png'
    
    final_img = q3.superimpose(text_image_path,depth_image_path,background_image_path)