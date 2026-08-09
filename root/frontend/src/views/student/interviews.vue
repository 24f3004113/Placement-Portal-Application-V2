<template>

    <h2>My Interviews</h2>

    <table border="1">

        <tbody>

            <tr>
                <th>Company</th>
                <th>Job Title</th>
                <th>Date</th>
                <th>Time</th>
                <th>Mode</th>
                <th>Link</th>
                <th>Location</th>
                <th>Remarks</th>
            </tr>

            <tr v-for="i in interviews" :key="i.iid">

                <td>{{ i.company }}</td>
                <td>{{ i.job_title }}</td>
                <td>{{ i.date }}</td>
                <td>{{ i.time }}</td>
                <td>{{ i.mode }}</td>

                <td>
                    <a v-if="i.link" :href="i.link.startsWith('http') ? i.link : 'https://' + i.link" target="_blank">
                        Join Interview
                    </a>
                    <span v-else>N/A</span>
                </td>

                <td>{{ i.location || "N/A" }}</td>
                <td>{{ i.remarks || "N/A" }}</td>

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
            interviews: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://127.0.0.1:5000/student/interviews",
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
            this.interviews = data
        else
            this.message = data.message || data.msg
    }

}

</script>