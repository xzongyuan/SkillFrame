# 使用示例

## 示例1: 基础用法

```javascript
const SkillTemplate = require('./src/index');

const skill = new SkillTemplate();
const result = await skill.execute({
  skillName: 'my-skill',
  description: 'My first skill'
});

console.log(result);
```

## 示例2: 自定义配置

```javascript
const skill = new SkillTemplate({
  mode: 'advanced',
  verbose: true
});
```