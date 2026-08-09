<template>

<h2>Application History</h2>

<table border="1">

<tbody>

<tr>
    <th>Status</th>
    <th>Feedback</th>
    <th>Updated On</th>
</tr>

<tr v-for="(h, index) in history" :key="index">
    <td>{{ h.status }}</td>
    <td>{{ h.feedback || "N/A" }}</td>
    <td>{{ h.updated_at }}</td>
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
            history: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://127.0.0.1:5000/student/application/" +
            this.$route.params.aid +
            "/history",
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

        if (response.ok) {
            this.history = data
        } else {
            this.message = data.message || data.msg
        }

    }

}

</script>