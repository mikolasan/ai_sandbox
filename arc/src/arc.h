#include <map>
#include <string>

// some round symbols take extra space,
// so I'm replacing them with other symbols of the same color
static std::map<int, std::string> color_map = {
  {0, "⚫️"}, // black
  {1, "🔵"}, // blue
  {2, "🔴"}, // red
  {3, "🍏"}, // green
  {4, "🍋"}, // yellow
  {5, "⚪️"}, // grey
  {6, "💗"}, // fuschia (pink)
  {7, "🟠"}, // orange
  {8, "🔮"}, // teal (light blue)
  {9, "🟤"}, // brown
};