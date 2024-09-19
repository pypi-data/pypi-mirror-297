# pycalfhello/post_install.py

def run_post_install():
    with open('post_install_log.txt', 'w') as f:
        f.write("Post-installation script executed successfully!")
