<template>

<h2>My Placement</h2>

<table border="1">

<tbody>

<tr>
    <th>Company</th>
    <th>Position</th>
    <th>Salary</th>
    <th>Joining Date</th>
</tr>

<tr v-for="p in placements" :key="p.company + p.position">

    <td>{{ p.company }}</td>
    <td>{{ p.position }}</td>
    <td>{{ p.salary }}</td>
    <td>{{ p.joining_date }}</td>

</tr>

</tbody>
</table>

<p>{{ message }}</p>

<button @click="$router.back()">Back</button>

</template>

<script>

export default {

    data() {
        return {
            placements: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://127.0.0.1:5000/student/placements",
            {
                headers: {
                    "Authorization":
                        "Bearer " + localStorage.getItem("token")
                },
                credentials: "include"
            }
        )

        let data = await response.json()

        if (response.status == 401 && data.msg == "Token has expired") {

            alert("Session expired. Please login again.")
            localStorage.removeItem("token")
            this.$router.push("/")
            return

        }

        if (response.ok)
            this.placements = data
        else
            this.message = data.message || data.msg

    }

}

</script>