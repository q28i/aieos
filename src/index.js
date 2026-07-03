const { exec } = require('child_process');
const path = require('path');
const util = require('util');
const execPromise = util.promisify(exec);

/**
 * Helper to run the AIEOS Python CLI with the --json flag.
 */
async function runAieosCommand(args) {
    // Determine path to the Python CLI script
    const cliPath = path.join(__dirname, '..', 'aieos.py');
    const command = `python "${cliPath}" ${args.join(' ')} --json`;
    
    try {
        const { stdout, stderr } = await execPromise(command);
        if (stdout) {
            try {
                // The CLI output should be pure JSON if --json was respected.
                return JSON.parse(stdout.trim());
            } catch (parseError) {
                // If it isn't JSON, throw a helpful error
                throw new Error(`Failed to parse AIEOS output as JSON. Output was:\n${stdout}`);
            }
        }
        return null;
    } catch (err) {
        throw new Error(`AIEOS Execution Error: ${err.message}`);
    }
}

/**
 * Search the AIEOS capability registry for skills matching the query.
 * @param {string} query - The search term (e.g. 'trading')
 * @returns {Promise<Array>} List of capability objects.
 */
async function searchSkills(query) {
    return await runAieosCommand(['skill', 'search', `"${query}"`]);
}

/**
 * Install an AIEOS capability package into the current workspace.
 * @param {string} packageName - The capability name to install.
 * @returns {Promise<Object>} Installation result.
 */
async function installSkill(packageName) {
    return await runAieosCommand(['skill', 'install', `"${packageName}"`]);
}

/**
 * Remove an AIEOS capability package from the current workspace.
 * @param {string} packageName - The capability name to remove.
 * @returns {Promise<Object>} Removal result.
 */
async function removeSkill(packageName) {
    return await runAieosCommand(['skill', 'remove', `"${packageName}"`]);
}

/**
 * Get recommendations based on project context.
 * @param {string} projectContext - Context string describing the project.
 * @returns {Promise<Array>} List of recommended capabilities.
 */
async function recommendSkills(projectContext) {
    return await runAieosCommand(['skill', 'recommend', `"${projectContext}"`]);
}

/**
 * Set the execution mode for the workspace.
 * @param {string} mode - The mode to set (e.g., 'trading', 'startup').
 * @returns {Promise<Object>} Mode update result.
 */
async function setExecutionMode(mode) {
    return await runAieosCommand(['mode', `"${mode}"`]);
}

module.exports = {
    searchSkills,
    installSkill,
    removeSkill,
    recommendSkills,
    setExecutionMode
};
