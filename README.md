# Artificial neural network sandbox

TODO: add description here. PRs are welcome ;)


## Install & Run

Pages from the `gui` folder are served by **vite**. Install modules

```
yarn install
```

Run in develpment mode

```
yarn dev
```

And open in the browser http://localhost:5173/

Other available pages:

- http://localhost:5173/emotions.html - dynamic model of emotions (only one bar)
- http://localhost:5173/index.html - artificial network visualization (WIP)
- http://localhost:5173/inverse-dynamics.html - 3D environment with a rolling wheel (solving with Euler and Newton equations)
- http://localhost:5173/qu-robot.html - visualization for **Qu Robot** project
- http://localhost:5173/robot-go.html - robot on a grid following the aim by listening ANN from the backend


### Backend for robot-go

Install dependencies

```
pip3 install --user -r requirements.txt
```

Run

```
python run-backend.py
```


## Links and notes

### PIXI js

- Guide https://pixijs.io/guides/basics/scene-graph.html
- API https://pixijs.download/release/docs/PIXI.Text.html

### A-star

- https://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html
- https://will.thimbleby.net/a-shortest-path-in-javascript/


### Polar plot

- https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_demo.html
- point colored by another vector https://stackoverflow.com/questions/14885895/color-by-column-values-in-matplotlib


### Pytorch

- mse loss https://pytorch.org/docs/stable/generated/torch.nn.MSELoss.html?highlight=mseloss


### Non-binary classifaction

- good article https://towardsdatascience.com/applied-deep-learning-part-1-artificial-neural-networks-d7834f67a4f6#106c
- notebook https://github.com/ardendertat/Applied-Deep-Learning-with-Keras/blob/master/notebooks/Part%201%20-%20Artificial%20Neural%20Networks.ipynb

n classes > 2 --> categorization / one-hot encoding --> softmax activation function
