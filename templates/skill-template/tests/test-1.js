// 测试文件
const SkillTemplate = require('../src/index');

async function test() {
  console.log('Running tests...\n');

  // 测试1: 基础功能
  try {
    const skill = new SkillTemplate();
    const result = await skill.execute({ test: true });
    console.log('✓ Test 1 passed: Basic execution');
    console.log('  Result:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('✗ Test 1 failed:', error.message);
  }

  // 测试2: 自定义配置
  try {
    const skill = new SkillTemplate({ mode: 'test', verbose: true });
    console.log('✓ Test 2 passed: Custom config');
    console.log('  Config:', skill.config);
  } catch (error) {
    console.error('✗ Test 2 failed:', error.message);
  }

  console.log('\nTests completed.');
}

test();