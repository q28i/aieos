const { searchSkills } = require('./core/index');

async function test() {
    console.log("Testing AIEOS JS SDK...");
    try {
        const results = await searchSkills("trading");
        console.log("SUCCESS. Parsed JSON Results:");
        console.log(JSON.stringify(results, null, 2));
    } catch (err) {
        console.error("FAILED.");
        console.error(err);
    }
}

test();
