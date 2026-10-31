#include <algorithm>
#include <charconv>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

struct Group {
  std::vector<uint32_t> latencies;
  uint64_t errors = 0;
};

uint32_t number(const std::string &line, size_t start, size_t end) {
  uint32_t value;
  auto [ptr, error] =
      std::from_chars(line.data() + start, line.data() + end, value);
  if (error != std::errc{} || ptr != line.data() + end)
    throw std::runtime_error("invalid integer");
  return value;
}

int main(int argc, char **argv) {
  try {
    std::filesystem::path data = "/data", out = "/out";
    for (int i = 1; i < argc; i += 2) {
      if (i + 1 == argc)
        throw std::runtime_error("expected --data DIR or --out DIR");
      std::string option = argv[i];
      if (option == "--data")
        data = argv[i + 1];
      else if (option == "--out")
        out = argv[i + 1];
      else
        throw std::runtime_error("unknown option");
    }
    std::ifstream input(data / "requests.log", std::ios::binary);
    if (!input)
      throw std::runtime_error("cannot open requests.log");
    std::unordered_map<std::string, Group> groups;
    std::string line;
    while (std::getline(input, line)) {
      if (line.size() < 39 || line[27] != ' ')
        throw std::runtime_error("invalid log line");
      const size_t method_end = line.find(' ', 28);
      if (method_end == std::string::npos)
        throw std::runtime_error("missing endpoint");
      const size_t endpoint_end = line.find(' ', method_end + 1);
      if (endpoint_end == std::string::npos ||
          endpoint_end + 5 >= line.size() || line[endpoint_end + 4] != ' ')
        throw std::runtime_error("invalid status field");
      const auto status = number(line, endpoint_end + 1, endpoint_end + 4);
      if (status < 100 || status > 599)
        throw std::runtime_error("status outside contract");
      const auto latency = number(line, endpoint_end + 5, line.size());
      // Fixed UTC hour text sorts chronologically; do not assume input order.
      auto key = line.substr(0, 13) + " " +
                 line.substr(method_end + 1, endpoint_end - method_end - 1);
      auto &group = groups[key];
      group.latencies.push_back(latency);
      group.errors += status >= 500;
    }
    if (!input.eof())
      throw std::runtime_error("input read failed");
    std::vector<decltype(groups)::value_type *> ordered;
    ordered.reserve(groups.size());
    for (auto &entry : groups)
      ordered.push_back(&entry);
    std::sort(ordered.begin(), ordered.end(),
              [](auto a, auto b) { return a->first < b->first; });
    std::filesystem::create_directories(out);
    std::ofstream output(out / "summary.txt", std::ios::binary);
    if (!output)
      throw std::runtime_error("cannot open summary.txt");
    for (auto entry : ordered) {
      auto &values = entry->second.latencies;
      std::sort(values.begin(), values.end());
      const uint64_t n = values.size(), errors = entry->second.errors;
      auto percentile = [&](uint64_t p) {
        return values[(p * n + 99) / 100 - 1];
      };
      output << entry->first.substr(0, 13) << ":00:00Z"
             << entry->first.substr(13) << ' ' << n << ' ' << percentile(50)
             << ' ' << percentile(95) << ' ' << percentile(99) << ' ' << errors
             << ' ' << errors * 1000000 / n << '\n';
    }
    output.close();
    if (!output)
      throw std::runtime_error("output write failed");
    return 0;
  } catch (const std::exception &error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
