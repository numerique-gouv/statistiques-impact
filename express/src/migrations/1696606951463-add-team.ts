import { MigrationInterface, QueryRunner } from "typeorm";

export class AddTeam1696606951463 implements MigrationInterface {
    name = 'AddTeam1696606951463'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "team" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying NOT NULL, CONSTRAINT "UQ_cf461f5b40cf1a2b8876011e1e1" UNIQUE ("name"), CONSTRAINT "PK_f57d8293406df4af348402e4b74" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "product" ADD "teamId" uuid`);
        await queryRunner.query(`ALTER TABLE "product" ADD CONSTRAINT "FK_851e921c51b7f69dd25a8e31392" FOREIGN KEY ("teamId") REFERENCES "team"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "product" DROP CONSTRAINT "FK_851e921c51b7f69dd25a8e31392"`);
        await queryRunner.query(`ALTER TABLE "product" DROP COLUMN "teamId"`);
        await queryRunner.query(`DROP TABLE "team"`);
    }

}
