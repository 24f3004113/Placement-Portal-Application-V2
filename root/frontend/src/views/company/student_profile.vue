<template>

    <div class="container mt-4">
        <h2 class="text-center">Student Profile</h2>

        <div class="row justify-content-center">
            <div class="col-md-6">

                <table class="table table-borderless table-light" v-if="student">
                    <tbody>
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
        <p v-if="student && !student.resume">
            Resume not uploaded
        </p>


    </div>

    <div v-if="student && student.resume" class="text-center">

        <h3>Resume</h3>

        <iframe :src="'http://localhost:5000/static/resumes/' + student.resume" width="700" height="990">
        </iframe>

    </div>
    <div class="text-center mt-3">
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
            "http://localhost:5000/company/application/" +
            this.$route.params.aid +
            "/student",
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