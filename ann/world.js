import { Node } from './astar.js';

const calc_distance = (x1, y1, x2, y2) => {
  let d_x = x2 - x1;
  let d_y = y1 - y2; // y axe is swapped
  return Math.sqrt(d_x * d_x + d_y * d_y);
}

const calc_angle = (x1, y1, x2, y2) => {
  let d_x = x2 - x1;
  let d_y = y1 - y2; // y axe is swapped
  let a = Math.atan(d_y / d_x);
  if (x1 <= x2) {
    a += Math.PI;
  } else if (y1 > y2) {
    a += 2 * Math.PI;
  }
  return a * 180 / Math.PI;
}

const y_cell = 64;
const y_lines = 5;

const x_cell = 64;
const x_lines = 5;

const grid = [];
for (let x = 0; x < x_lines; ++x) {
  grid.push([]);
  for (let y = 0; y < y_lines; ++y) {
    grid[x].push(new Node(x, y, false, grid))
  }
}

export { calc_angle, calc_distance, x_cell, y_cell, x_lines, y_lines, grid }