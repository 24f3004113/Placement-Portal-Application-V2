<template>

    <h2>Student Applications</h2>

    <p>Student: {{ student }}</p>
    <p>Email: {{ email }}</p>
    <p>Phone No.: {{ phone }}</p>
    <p>Course: {{ course }}</p>
    <p>CGPA: {{ cgpa }}</p>

    <table border="1">

        <thead>
            <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Application Date</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>

        <tbody>

            <tr v-if="applications.length == 0">
                <td colspan="5">No applications found</td>
            </tr>

            <tr v-for="application in applications" :key="application.aid">

                <td>{{ application.aid }}</td>
                <td>{{ application.company }}</td>
                <td>{{ application.job_title }}</td>
                <td>{{ application.application_date }}</td>
                <td>{{ application.status }}</td>
                <td>
                    <button @click="$router.push('/admin/student/' + application.sid)">View Student</button>
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
            student: "",
            email: "",
            phone: "",
            course: "",
            cgpa: "",
            applications: [],
            message: ""
        }
    },

    methods: {

        async getApplications() {

            let response = await fetch(
                "http://127.0.0.1:5000/admin/student/" +
                this.$route.params.sid +
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
                this.student = data.student
                this.email = data.email
                this.phone = data.phone,
                    this.course = data.course,
                    this.cgpa = data.cgpa
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