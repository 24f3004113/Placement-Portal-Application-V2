<template>



    <h2>Application History</h2>



    <div v-if="application">

        <div class="container my-5 shadow p-2 ">
            <div class="table-responsive-md">
                <table class="table table-striped  table-bordered table-hover ">

                    <tbody>

                        <tr>
                            <td>Application No.</td>
                            <td>{{ application.aid }}</td>
                        </tr>

                        <tr>
                            <td>Student</td>
                            <td>{{ application.student }}</td>
                        </tr>

                        <tr>
                            <td>Course</td>
                            <td>{{ application.course }}</td>
                        </tr>

                        <tr>
                            <td>Skills</td>
                            <td>{{ application.skills }}</td>
                        </tr>

                        <tr>
                            <td>CGPA</td>
                            <td>{{ application.cgpa }}</td>
                        </tr>

                        <tr>
                            <td>Company</td>
                            <td>{{ application.company }}</td>
                        </tr>

                        <tr>
                            <td>Applied Position</td>
                            <td>{{ application.job_title }}</td>
                        </tr>

                        <tr>
                            <td>Application Date</td>
                            <td>{{ application.application_date }}</td>
                        </tr>

                        <tr>
                            <td>Current Status</td>
                            <td>{{ application.status }}</td>
                        </tr>

                    </tbody>

                </table>
            </div>
        </div>

        <br>

        <h3>Status History</h3>

        <div class="container my-5 shadow p-2 ">
            <div class="table-responsive-md">
                <table class="table table-striped  table-bordered table-hover ">

                    <tbody>

                        <tr>
                            <th>Status</th>
                            <th>Feedback</th>
                            <th>Updated At</th>
                        </tr>

                        <tr v-for="h in application.history" :key="h.hid">
                            <td>{{ h.status }}</td>
                            <td>{{ h.feedback || "N/A" }}</td>
                            <td>{{ h.updated_at }}</td>
                        </tr>

                    </tbody>


                </table>
            </div>
        </div>

    </div>

    <p>{{ message }}</p>

    <button @click="$router.back()">Back</button>

</template>

<script>

export default {

    data() {
        return {
            application: null,
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/admin/application/" +
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

        if ( data.msg == "Token has expired") {
            alert("Session expired. Please login again.")
            localStorage.removeItem("token")
            this.$router.push("/")
            return
        }

        if (response.ok)
            this.application = data
        else
            this.message = data.message || data.msg

    }

}

</script>
