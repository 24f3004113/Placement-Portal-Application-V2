<template>
    <div class="text-center">
        <h2>Companies</h2>

        <br>


        <input type="text" placeholder="Search" v-model="search" @input="getCompanies">

        <select v-model="approvalFilter" @change="getCompanies">
            <option value="">All Approval Status</option>
            <option value="Pending">Pending</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
        </select>

        <select v-model="blockedFilter" @change="getCompanies">
            <option value="">All</option>
            <option value="true">Blocked</option>
            <option value="false">Not Blocked</option>
        </select>

        <button @click="clearFilters">Clear</button>
    </div>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Company</th>
                        <th>Email</th>
                        <th>Industry</th>
                        <th>Location</th>
                        <th>HR Contact</th>
                        <th>Website</th>
                        <th>Approval</th>
                        <th>Blacklist Status</th>
                        <th>Actions</th>
                        <th>Blacklist</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="companies.length == 0">
                        <td colspan="11" class="text-xxl-center">No companies found</td>
                    </tr>

                    <tr v-else v-for="company in companies" :key="company.cid">

                        <td>{{ company.cid }}</td>
                        <td>{{ company.company_name }}</td>
                        <td>{{ company.email }}</td>
                        <td>{{ company.industry }}</td>
                        <td>{{ company.location }}</td>
                        <td>{{ company.hr_contact }}</td>
                        <td>{{ company.website }}</td>
                        <td>{{ company.approval_status }}</td>
                        <td>{{ company.blacklisted ? "Blocked" : "Not Blocked" }}</td>

                        <td>
                            <button class="bg-primary btn shadow text-white me-2"
                                @click="$router.push('/admin/company/' + company.cid + '/drives')">
                                View Drives
                            </button>

                            <button v-if="company.approval_status == 'Pending'"
                                class="bg-success btn shadow text-white me-2" @click="approve(company.cid)">
                                Approve
                            </button>

                            <button v-if="company.approval_status == 'Pending'" class="bg-danger btn shadow text-white"
                                @click="reject(company.cid)">
                                Reject
                            </button>
                        </td>

                        <td>
                            <button v-if="!company.blacklisted" class="bg-danger btn shadow text-white"
                                @click="blacklist(company.cid)">
                                Blacklist
                            </button>

                            <button v-else class="bg-success btn shadow text-white" @click="unblacklist(company.cid)">
                                Unblacklist
                            </button>
                        </td>

                    </tr>

                </tbody>

            </table>
        </div>
    </div>

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
            companies: [],
            search: "",
            approvalFilter: "",
            blockedFilter: ""
        }

    },

    methods: {

        async getCompanies() {

            let response = await fetch(
                "http://localhost:5000/admin/companies?search=" + this.search +
                "&approval_status=" + this.approvalFilter +
                "&blacklisted=" + this.blockedFilter,
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.companies = await response.json()

        },

        async approve(cid) {

            await fetch(
                "http://localhost:5000/admin/company/" + cid + "/approve",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async reject(cid) {

            await fetch(
                "http://localhost:5000/admin/company/" + cid + "/reject",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async blacklist(cid) {

            await fetch(
                "http://localhost:5000/admin/company/" + cid + "/blacklist",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async unblacklist(cid) {

            await fetch(
                "http://localhost:5000/admin/company/" + cid + "/unblacklist",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },
        clearFilters() {

            this.search = ""
            this.approvalFilter = ""
            this.blockedFilter = ""

            this.getCompanies()

        }

    },

    mounted() {

        this.getCompanies()

    }

}

</script>