<template>

    <h2 class="text-center">Drive Details</h2>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <table class="table table-bordered border-dark" v-if="drive">


                <tbody>
                    <tr>
                        <td>Company</td>
                        <td>{{ drive.company }}</td>
                    </tr>
                    <tr>
                        <td>Job Title</td>
                        <td>{{ drive.job_title }}</td>
                    </tr>
                    <tr>
                        <td>Description</td>
                        <td>{{ drive.description }}</td>
                    </tr>
                    <tr>
                        <td>Course</td>
                        <td>{{ drive.course }}</td>
                    </tr>
                    <tr>
                        <td>Minimum CGPA</td>
                        <td>{{ drive.min_cgpa }}</td>
                    </tr>
                    <tr>
                        <td>Graduation Year</td>
                        <td>{{ drive.graduation_year }}</td>
                    </tr>
                    <tr>
                        <td>Salary</td>
                        <td>{{ drive.salary }}</td>
                    </tr>
                    <tr>
                        <td>Deadline</td>
                        <td>{{ drive.deadline }}</td>
                    </tr>
                    <tr>
                        <td>Approval Status</td>
                        <td>{{ drive.approval_status }}</td>
                    </tr>
                    <tr>
                        <td>Status</td>
                        <td>{{ drive.status }}</td>
                    </tr>
                    <tr>
                        <td>Applications Received</td>
                        <td>{{ drive.application_count }}</td>
                    </tr>
                </tbody>

            </table>
        </div>
    </div>

    <p>{{ message }}</p>

    <div class="text-center mt-3">
        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin')">
            Dashboard
        </button>
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>
        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
    </div>

</template>

<script>

export default {

    data() {
        return {
            drive: null,
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/admin/drive/" +
            this.$route.params.did,
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

        if (response.ok)
            this.drive = data
        else
            this.message = data.message || data.msg
    }

}

</script>