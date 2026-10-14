// Export raw experiment data from browser to CSV or JSON
function exportSimulationData(historyF, historyLr, historyCap, historyInh, historyLrn, gens) {
    let rows = [["Generation", "Retention_f", "LearningRate_lr", "Capacity_c", "Percent_Inherited", "Percent_Learned"]];
    for (let i = 0; i < gens.length; i++) {
        rows.push([
            gens[i],
            historyF[i].toFixed(4),
            (historyLr[i] / 10).toFixed(4),
            historyCap[i].toFixed(4),
            historyInh[i].toFixed(2),
            historyLrn[i].toFixed(2)
        ]);
    }
    let csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `matrix_gal_run_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
