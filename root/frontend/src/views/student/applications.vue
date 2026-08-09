<template>

    <h2>My Applications</h2>

    <button @click="exportApplications">
        Export Applications
    </button>

    <button @click="downloadApplications">
        Download CSV
    </button>

    <p>{{ message }}</p>

    <table border="1">

        <tbody>

            <tr>
                <th>Company</th>
                <th>Job Title</th>
                <th>Application Date</th>
                <th>Status</th>
                <th>Feedback</th>
                <th>Drive</th>
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
                    <button @click="$router.push('/student/application/' + a.aid + '/history')">
                        History
                    </button>
                </td>

            </tr>

        </tbody>

    </table>


</template>

<script>

export default {

    data() {
        return {
            applications: [],
            message: ""
        }
    },
    methods: {

        async exportApplications() {

            let response = await fetch(
                "http://localhost:5000/student/export/applications",
                {
                    headers: {
                        Authorization:
                            "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            let data = await response.json()

            this.message = data.message
        },

        async downloadApplications() {

            let response = await fetch(
                "http://localhost:5000/student/export/applications/download",
                {
                    headers: {
                        Authorization:
                            "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            if (!response.ok) {

                this.message = "CSV is not ready yet"

                return
            }

            let blob = await response.blob()

            let url = window.URL.createObjectURL(blob)

            let link = document.createElement("a")

            link.href = url
            link.download = "applications.csv"

            link.click()

            window.URL.revokeObjectURL(url)
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