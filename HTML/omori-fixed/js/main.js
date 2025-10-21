//=============================================================================
// main.js
//=============================================================================

PluginManager.setup($plugins);

window.onload = function() {
    SceneManager.run(Scene_Boot);
    setTimeout(() => {
        window.fullSetupComplete = true;
    }, 2500);
};
