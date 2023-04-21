
export function searchFilter(){
    console.log("in search filter function");
    const filterForm = document.getElementById("filterForm");
    const sortBy = filterForm.sortBy.value;
    const marketName = filterForm.marketName.value;
    const closestSupermarket = filterForm.closestSupermarket.checked;

    let queryParams = new URLSearchParams();
    queryParams.set("sortBy", sortBy);
    queryParams.set("marketName", marketName);
    queryParams.set("closestSupermarket", closestSupermarket);

    window.location.href = "/browse?" + queryParams.toString();
}