# vocabtestsolver
Deployed <a href="http://vocabtestsolver.duckdns.org/">here!</a> -- Not  anymore!

Use python 3.6 to avoid some compatibility issues. Conda is probably your best
bet:
```
conda create --name vocabtest_env python=3.6
conda activate vocabtest_env
pip install -r requirements.txt
```
Then, to run:
```
python main.py
```
Navigate to `localhost:8000` in your browser to use.