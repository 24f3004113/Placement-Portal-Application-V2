<template>

    <h2>My Applications</h2>

    <table border="1">

        <tbody>

            <tr>
                <th>Company</th>
                <th>Job Title</th>
                <th>Application Date</th>
                <th>Status</th>
                <th>Feedback</th>
                <th>Drive</th>
                <th>Interview</th>
                <th>History</th>
            </tr>

            <tr v-for="a in applications" :key="a.aid">

                <td>{{ a.company }}</td>
                <td>{{ a.job_title }}</td>
                <td>{{ a.application_date }}</td>
                <td>{{ a.status }}</td>
                <td>{{ a.feedback }}</td>

                <td>
                    <button @click="$router.push('/student/drive/' + a.did)">
                        View Drive
                    </button>
                </td>

                <td>
                    <button v-if="a.interview" @click="$router.push('/student/application/' + a.aid + '/interview')">
                        View Interview
                    </button>

                    <span v-else>Not Scheduled</span>
                </td>

                <td>
                    <button @click="$router.push('/student/application/' + a.aid + '/history')">
                        History
                    </button>
                </td>

            </tr>

        </tbody>

    </table>

    <p>{{ message }}</p>

</template>

<script>

export default {

    data() {
        return {
            applications: [],
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://127.0.0.1:5000/student/applications",
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
            this.applications = data
        else
            this.message = data.message || data.msg
    }

}

</script>