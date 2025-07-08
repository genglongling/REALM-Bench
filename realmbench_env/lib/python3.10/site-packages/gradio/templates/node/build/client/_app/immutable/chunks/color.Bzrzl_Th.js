import { o as ordered_colors } from "./2.Dc6zh421.js";
const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};
export {
  get_next_color as g
};
