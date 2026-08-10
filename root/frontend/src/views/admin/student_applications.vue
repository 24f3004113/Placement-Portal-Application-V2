<template>

    <h2 class="text-center">Student Applications</h2>

    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">

                <table class="table table-bordered table-hover shadow">

                    <tbody>


                        <tr>
                            <td>Student</td>
                            <td>{{ student }}</td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>{{ email }}</td>
                        </tr>
                        <tr>
                            <td>Phone No.</td>
                            <td>{{ phone }}</td>
                        </tr>
                        <tr>
                            <td>Course</td>
                            <td>{{ course }}</td>
                        </tr>


                        <tr>
                            <td>CGPA</td>
                            <td>{{ cgpa }}</td>
                        </tr>





                    </tbody>

                </table>
            </div>
        </div>
    </div>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

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
                            <button class="bg-primary btn shadow text-white me-2"
                                @click="$router.push('/admin/student/' + application.sid)">
                                View Student
                            </button>

                            <button class="bg-secondary btn shadow text-white"
                                @click="$router.push('/admin/application/' + application.aid + '/history')">
                                History
                            </button>
                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>

    <br>

    <div class="text-center mt-3">
        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin')">
            Dashboard
        </button>
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>
        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
    </div>

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
                "http://localhost:5000/admin/student/" +
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

            if (data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

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