<template>

    <h2>Drive Applications</h2>

    <table v-if="drive">
        <tbody>
            <tr>
                <td>Company:</td>
                <td>{{ company }}</td>
            </tr>

            <tr>
                <td>Job Title:</td>
                <td>{{ drive }}</td>
            </tr>
        </tbody>


    </table>

    <br>

    <table border="1">

        <thead>
            <tr>
                <th>ID</th>
                <th>Student</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Course</th>
                <th>CGPA</th>
                <th>Application Date</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            <tr v-if="applications.length == 0">
                <td colspan="9">No applications found</td>
            </tr>

            <tr v-for="application in applications" :key="application.aid">

                <td>{{ application.aid }}</td>
                <td>{{ application.student }}</td>
                <td>{{ application.email }}</td>
                <td>{{ application.phone }}</td>
                <td>{{ application.course }}</td>
                <td>{{ application.cgpa }}</td>
                <td>{{ application.application_date }}</td>
                <td>{{ application.status }}</td>


                <td>
                    <button @click="$router.push('/company/application/' + application.aid + '/student')">
                        View Student
                    </button>
                </td>
                <td>
                    <button @click="$router.push('/company/application/' + application.aid + '/update')">
                        Update
                    </button>

                    <button v-if="application.status == 'Shortlisted'"
                        @click="$router.push('/company/application/' + application.aid + '/interview')">
                        Schedule Interview
                    </button>

                    <button v-if="application.status == 'Interview'"
                        @click="$router.push('/company/application/' + application.aid + '/interview/update')">
                        View / Update Interview
                    </button>


                </td>

            </tr>

        </tbody>

    </table>

    <br>

    <button @click="$router.back()">Back</button>

    <p>{{ message }}</p>

</template>

<script>

export default {

    data() {
        return {
            company: "",
            drive: "",
            applications: [],
            message: ""
        }
    },

    methods: {

        async getApplications() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/drive/" +
                this.$route.params.did +
                "/applications",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (response.ok) {
                this.company = data.company
                this.drive = data.drive
                this.applications = data.applications
            } else {
                this.message = data.message
            }

        }

    },

    mounted() {
        this.getApplications()
    }

}

</script>