import os
import shutil

STEREO_JS_SOURCE='example/stereo.js'
STEREO_JS_SOURCE_AR2 = 'example_ar_2_195/stereo.js'
SAVE_PATH = 'viewers'
# PAIRS_USER_STUDY_PATH = "https://michalgeyer.github.io/vr-viewer-files-webm/pairs-user-study-webm-stereocrafter"  # https path used inside <source>
VIDEOS_LOCAL_PATH = "stereocrafter-user-study"
PAIRS_USER_STUDY_PATH = VIDEOS_LOCAL_PATH


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>360 stereo video</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <link type="text/css" rel="stylesheet" href="../../css/main.css">
    <script type="importmap">
        {{
          "imports": {{
            "three": "https://cdn.jsdelivr.net/npm/three@0.166.1/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.166.1/examples/jsm/"
          }}
        }}
    </script>
</head>
<body>
    <div id="container" style="position: absolute; top: 50%; left: 50%; 
         transform: translate(-50%, -50%); display: flex; 
         justify-content: center; align-items: center; width: auto; height: auto;">
    </div>
    
    <video id="video" autoplay muted crossorigin="anonymous" playsinline style="display:none">
      <source src="{commented_path}" type="video/webm">
    </video>
    
    <script type="module" src="stereo.js"></script>
</body>
</html>
"""
#       <source src="{actual_path}" type="video/mp4">
def create_html(prompt_name: str, leftright: str, result: str) -> str:
    """
    Generate the HTML content for a given prompt and result.
    E.g. result can be 'ours' or 'depth_c'.
    """
    # commented_path = f"{PAIRS_USER_STUDY_PATH}/{leftright}/{prompt_name}/{result}.webm"
    commented_path = f"{PAIRS_USER_STUDY_PATH}/{prompt_name}/{result}.mp4"
    
    return HTML_TEMPLATE.format(
        commented_path=commented_path,
    )

def main():
    VIEWER_TYPE = 'spatial_compare' # | 'temporal_compare' | 'spatial_compare' | 'seperate'
    assert VIEWER_TYPE in ['seperate', 'temporal_compare', 'spatial_compare'], "Invalid viewer type"
    # Go through each item in the video folder
    # local_pairs_ours_left = os.path.join(VIDEOS_LOCAL_PATH, 'left')
    # local_pairs_ours_right = os.path.join(VIDEOS_LOCAL_PATH, 'right')
    # prompts_leftright = {prompt: 'left' for prompt in os.listdir(local_pairs_ours_left)}
    # prompts_leftright.update({prompt: 'right' for prompt in os.listdir(local_pairs_ours_right)})
    # for prompt, leftright in prompts_leftright.items():
    for prompt in os.listdir(VIDEOS_LOCAL_PATH):
        leftright = ''
        # if not 'kitchen' in prompt:
        #     continue
        print(prompt)
        if VIEWER_TYPE == 'seperate':
        # Create subfolders for each result type
            ours_folder = os.path.join(SAVE_PATH, f"{prompt}_ours")
            warp_inpaint_folder = os.path.join(SAVE_PATH, f"{prompt}_warp_inpaint")
            
            os.makedirs(ours_folder, exist_ok=True)
            os.makedirs(warp_inpaint_folder, exist_ok=True)
            
            # Generate the HTML for each result
            ours_html = create_html(prompt, leftright, "ours")
            warp_inpaint_html = create_html(prompt, leftright, "warp_inpaint")
            
            # Write index.html into each subfolder
            with open(os.path.join(ours_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(ours_html)
            
            with open(os.path.join(warp_inpaint_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(warp_inpaint_html)
            
            # Copy stereo.js to each subfolder
            shutil.copy2(STEREO_JS_SOURCE, ours_folder)
            shutil.copy2(STEREO_JS_SOURCE, warp_inpaint_folder)
            print(f"Created HTML for prompt: {prompt}")
        
        else:
            if prompt.startswith('.'):
                continue
            filename = 'comparison_temporal' if  VIEWER_TYPE == 'temporal_compare' else 'comparison_spatial'
            prompt_folder = os.path.join(SAVE_PATH, f"{prompt}_{filename}")
            os.makedirs(prompt_folder, exist_ok=True)
            
            # Generate the HTML for each result
            html = create_html(prompt, leftright, filename)
            
            # Write index.html into each subfolder
            with open(os.path.join(prompt_folder, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            shutil.copy2(STEREO_JS_SOURCE, prompt_folder) if VIEWER_TYPE == 'temporal_compare' else shutil.copy2(STEREO_JS_SOURCE_AR2, prompt_folder)

if __name__ == "__main__":
    main()
