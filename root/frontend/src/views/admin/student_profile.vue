<template>

    <h2 class="text-center">Student Profile</h2>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">

                <table class="table table-bordered table-hover shadow" v-if="student">



                    <tbody>

                        <tr>
                            <td>ID</td>
                            <td>{{ student.sid }}</td>
                        </tr>
                        <tr>
                            <td>Name</td>
                            <td>{{ student.name }}</td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>{{ student.email }}</td>
                        </tr>
                        <tr>
                            <td>Phone</td>
                            <td>{{ student.phone }}</td>
                        </tr>
                        <tr>
                            <td>Course</td>
                            <td>{{ student.course }}</td>
                        </tr>
                        <tr>
                            <td>CGPA</td>
                            <td>{{ student.cgpa }}</td>
                        </tr>
                        <tr>
                            <td>Graduation Year</td>
                            <td>{{ student.graduation_year }}</td>
                        </tr>
                        <tr>
                            <td>Skills</td>
                            <td>{{ student.skills }}</td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div v-if="student && student.resume" class="text-center">

        <h3>Resume</h3>

        <iframe :src="'http://localhost:5000/static/resumes/' + student.resume" width="700" height="990">
        </iframe>

    </div>

    <p v-else-if="student">Resume not uploaded</p>

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
            student: null,
            message: ""
        }
    },

    async mounted() {

        let response = await fetch(
            "http://localhost:5000/admin/student/" +
            this.$route.params.sid,
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
            this.student = data
        else
            this.message = data.message || data.msg
    }

}

</script>