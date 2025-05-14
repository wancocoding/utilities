

# Clash Rule

路径`files/configs/clash-rules`

## 使用方法

以Clash Verge为例,在客户端的规则脚本里添加
```
const ruleProviders = {
    // 省略
  "ChatGPT": {
    ...ruleProviderCommon,
    "behavior": "domain",
    "url": "https://raw.githubusercontent.com/wancocoding/utilities/refs/heads/main/files/configs/clash-rules/ai.txt",
    "path": "./ruleset/cocoding/Chatgpt.yaml"
  },
```
上面这段通常在规则集配置里,以及规则rule
```
// 规则
const rules = [
  // 自定义规则
  "RULE-SET,ChatGPT,ChatGPT",
];
```
和代理组,只能手动选择,因为代理可能会变,一般机场都会更新代理节点,所以
```
config["proxy-groups"] = [
    {
      ...groupBaseOption,
      "name": "ChatGPT",
      "type": "select",
      "include-all": true,
      "proxies": ["节点选择"],
      "icon": "https://fastly.jsdelivr.net/gh/clash-verge-rev/clash-verge-rev.github.io@main/docs/assets/icons/chatgpt.svg"
    },
]
```