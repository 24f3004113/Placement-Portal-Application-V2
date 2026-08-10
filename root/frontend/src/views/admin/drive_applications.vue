<template>

    <h2>Drive Applications</h2>

    <p><b>Company:</b> {{ company }}</p>
    <p><b>Job Title:</b> {{ drive }}</p>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

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
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="applications.length == 0">
                        <td colspan="8">No applications found</td>
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
                            <button @click="$router.push('/admin/student/' + application.sid)">View Student</button>
                            <button
                                @click="$router.push('/admin/application/' + application.aid + '/history')">History</button>
                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>

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
                "http://localhost:5000/admin/drive/" +
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

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

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