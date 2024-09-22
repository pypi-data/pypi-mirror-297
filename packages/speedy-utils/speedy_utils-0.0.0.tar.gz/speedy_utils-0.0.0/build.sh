# [mac>py312| ~/gitprojects/speedy ] cat_projects ./ | pbcopy                 
# get_text2print at /Users/anhvth/dotfiles/custom-tools/pytools-cat_projects.py:55: 100%|████████████████████████████████████████| 11/11 [00:00<00:00, 76895.57it/s]
# [mac>py312| ~/gitprojects/speedy ] rm -r build 
# [mac>py312| ~/gitprojects/speedy ] ls     
# README.md             dist                  pyproject.toml        speedy                speedy_utils.egg-info
# __pycache__           py_speedy.egg-info    report.md             speedy.egg-info       test.py
# [mac>py312| ~/gitprojects/speedy ] rm -r dist    
# [mac>py312| ~/gitprojects/speedy ] vi build.sh         
# [mac>py312| ~/gitprojects/speedy ] code build.sh           
# [mac>py312| ~/gitprojects/speedy ] 


rm -r build dist *.egg-info
python -m build
python -m twine upload --repository testpypi dist/*

